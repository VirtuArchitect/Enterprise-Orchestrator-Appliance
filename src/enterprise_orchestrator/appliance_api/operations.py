from __future__ import annotations

import json
import tarfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


ROOT = Path(__file__).resolve().parents[3]


def create_backup(output_dir: Path | None = None) -> dict[str, Any]:
    state = ensure_state_dir()
    output_dir = output_dir or ROOT / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    target = output_dir / f"enterprise-orchestrator-state-backup-{stamp}.tar.gz"
    with tarfile.open(target, "w:gz") as archive:
        for path in sorted(state.rglob("*")):
            if path.is_file():
                archive.add(path, arcname=path.relative_to(state))
    return {
        "backup_id": new_id("bak"),
        "path": str(target),
        "state_dir": str(state),
        "created_at": datetime.now(UTC).isoformat(),
    }


def stage_update(
    artifact_path: str,
    sha256: str,
    requested_by: str,
    version: str,
    notes: str = "",
) -> dict[str, Any]:
    if not artifact_path or not sha256:
        raise ValueError("artifact_path and sha256 are required")
    request = {
        "update_id": new_id("upd"),
        "artifact_path": artifact_path,
        "sha256": sha256,
        "requested_by": requested_by,
        "version": version,
        "notes": notes,
        "status": "staged",
        "apply_enabled": False,
        "created_at": datetime.now(UTC).isoformat(),
    }
    path = ensure_state_dir() / "updates.json"
    records = read_json(path, [])
    records.append(request)
    write_json(path, records)
    return request


def list_updates() -> list[dict[str, Any]]:
    return read_json(ensure_state_dir() / "updates.json", [])
