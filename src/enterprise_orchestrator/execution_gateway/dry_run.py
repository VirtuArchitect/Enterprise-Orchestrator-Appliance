from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


class DryRunExecutionGateway:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ensure_state_dir() / "executions.json"

    def execute(
        self,
        request_id: str,
        tenant: str,
        actor: str,
        plan: dict[str, Any],
        approved: bool,
        mode: str = "dry-run",
    ) -> dict[str, Any]:
        if mode != "dry-run":
            raise PermissionError("only dry-run execution is implemented")

        risk_tier = plan["risk_tier"]
        if risk_tier != "T0" and not approved:
            raise PermissionError("approval is required before dry-run execution")

        result = {
            "execution_id": new_id("exe"),
            "request_id": request_id,
            "tenant": tenant,
            "actor": actor,
            "mode": mode,
            "status": "completed",
            "risk_tier": risk_tier,
            "actions": [
                action["description"] for action in plan.get("recommended_actions", [])
            ],
            "created_at": datetime.now(UTC).isoformat(),
        }
        records = self.list()
        records.append(result)
        write_json(self.path, records)
        return result

    def list(self, tenant: str | None = None) -> list[dict[str, Any]]:
        records = read_json(self.path, [])
        if tenant is None:
            return records
        return [record for record in records if record.get("tenant") == tenant]
