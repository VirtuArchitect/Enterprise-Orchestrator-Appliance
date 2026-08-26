from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import append_jsonl, read_jsonl
from enterprise_orchestrator.paths import ensure_state_dir


GENESIS_HASH = "0" * 64


class AuditStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ensure_state_dir() / "audit.jsonl"

    def append(
        self,
        event_type: str,
        tenant: str,
        actor: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        records = self.list()
        previous_hash = records[-1]["event_hash"] if records else GENESIS_HASH
        event = {
            "event_id": new_id("aud"),
            "event_type": event_type,
            "tenant": tenant,
            "actor": actor,
            "payload": payload,
            "created_at": datetime.now(UTC).isoformat(),
            "previous_hash": previous_hash,
        }
        event["event_hash"] = _hash_event(event)
        append_jsonl(self.path, event)
        return event

    def list(self, tenant: str | None = None) -> list[dict[str, Any]]:
        records = read_jsonl(self.path)
        if tenant is None:
            return records
        return [record for record in records if record.get("tenant") == tenant]

    def verify_chain(self) -> bool:
        previous_hash = GENESIS_HASH
        for record in self.list():
            if record.get("previous_hash") != previous_hash:
                return False
            expected = _hash_event({k: v for k, v in record.items() if k != "event_hash"})
            if record.get("event_hash") != expected:
                return False
            previous_hash = record["event_hash"]
        return True


def _hash_event(event: dict[str, Any]) -> str:
    encoded = json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
