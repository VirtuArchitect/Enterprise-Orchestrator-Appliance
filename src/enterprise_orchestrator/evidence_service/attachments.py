from __future__ import annotations

import base64
from datetime import UTC, datetime
import hashlib
from pathlib import Path
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


MAX_ATTACHMENT_BYTES = 1024 * 1024


class EvidenceAttachmentStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or ensure_state_dir() / "evidence-attachments"
        self.index_path = self.root / "attachments.json"

    def add(
        self,
        tenant: str,
        submitted_by: str,
        filename: str,
        content_base64: str,
        classification: str = "operator_provided",
    ) -> dict[str, Any]:
        safe_name = _safe_filename(filename)
        try:
            content = base64.b64decode(content_base64, validate=True)
        except Exception as exc:
            raise ValueError("content_base64 is not valid base64") from exc
        if len(content) > MAX_ATTACHMENT_BYTES:
            raise ValueError("attachment exceeds 1048576 byte limit")

        attachment_id = new_id("att")
        storage_path = self.root / f"{attachment_id}.bin"
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        storage_path.write_bytes(content)

        record = {
            "attachment_id": attachment_id,
            "tenant": tenant,
            "submitted_by": submitted_by,
            "filename": safe_name,
            "classification": classification,
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "storage_path": storage_path.relative_to(ensure_state_dir()).as_posix(),
            "created_at": datetime.now(UTC).isoformat(),
        }
        records = self.list()
        records.append(record)
        write_json(self.index_path, records)
        return record

    def list(self, tenant: str | None = None) -> list[dict[str, Any]]:
        records = read_json(self.index_path, [])
        if tenant is None:
            return records
        return [record for record in records if record.get("tenant") == tenant]


def _safe_filename(filename: str) -> str:
    raw = (filename or "").strip()
    if "/" in raw or "\\" in raw:
        raise ValueError("filename must not include a path")
    candidate = Path(raw).name.strip()
    if not candidate or candidate in {".", ".."}:
        raise ValueError("filename is required")
    if candidate != filename.strip():
        raise ValueError("filename must not include a path")
    return candidate
