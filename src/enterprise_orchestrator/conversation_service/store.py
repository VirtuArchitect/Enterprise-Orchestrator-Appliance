from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


VALID_ROLES = {"system", "user", "assistant", "tool"}


class ConversationStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ensure_state_dir() / "conversations.json"

    def create(self, tenant: str, operator: str, title: str) -> dict[str, Any]:
        records = self.list()
        now = _now()
        record = {
            "conversation_id": new_id("cnv"),
            "tenant": tenant,
            "operator": operator,
            "title": title.strip() or "Untitled conversation",
            "created_at": now,
            "updated_at": now,
            "messages": [],
        }
        records.append(record)
        write_json(self.path, records)
        return record

    def append(
        self,
        conversation_id: str,
        tenant: str,
        operator: str,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if role not in VALID_ROLES:
            raise ValueError(f"invalid conversation message role: {role}")
        records = self.list()
        for record in records:
            if record["conversation_id"] == conversation_id and record["tenant"] == tenant:
                message = {
                    "message_id": new_id("msg"),
                    "role": role,
                    "content": content,
                    "operator": operator,
                    "metadata": metadata or {},
                    "created_at": _now(),
                }
                record["messages"].append(message)
                record["updated_at"] = message["created_at"]
                write_json(self.path, records)
                return record
        raise KeyError(f"conversation not found: {conversation_id}")

    def list(
        self,
        tenant: str | None = None,
        operator: str | None = None,
    ) -> list[dict[str, Any]]:
        records = read_json(self.path, [])
        if tenant is not None:
            records = [record for record in records if record.get("tenant") == tenant]
        if operator is not None:
            normalized = operator.strip().lower()
            records = [
                record
                for record in records
                if record.get("operator", "").strip().lower() == normalized
            ]
        return sorted(records, key=lambda record: record.get("updated_at", ""), reverse=True)

    def get(self, conversation_id: str, tenant: str) -> dict[str, Any]:
        for record in self.list(tenant=tenant):
            if record["conversation_id"] == conversation_id:
                return record
        raise KeyError(f"conversation not found: {conversation_id}")


def _now() -> str:
    return datetime.now(UTC).isoformat()
