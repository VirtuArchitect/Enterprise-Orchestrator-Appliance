from __future__ import annotations

from typing import Any

from enterprise_orchestrator.json_store import read_json
from enterprise_orchestrator.paths import ensure_state_dir


def list_requests(tenant: str | None = None) -> list[dict[str, Any]]:
    records = read_json(ensure_state_dir() / "requests.json", [])
    if tenant is None:
        return records
    return [record for record in records if record.get("tenant") == tenant]
