from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


class ApprovalQueue:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ensure_state_dir() / "approvals.json"

    def create(
        self,
        request_id: str,
        tenant: str,
        requested_by: str,
        risk_tier: str,
        reason: str,
        plan_hash: str,
    ) -> dict[str, Any]:
        approvals = self.list()
        existing = [
            item
            for item in approvals
            if item["request_id"] == request_id and item["status"] == "pending"
        ]
        if existing:
            return existing[0]

        record = {
            "approval_id": new_id("apr"),
            "request_id": request_id,
            "tenant": tenant,
            "requested_by": requested_by,
            "risk_tier": risk_tier,
            "reason": reason,
            "plan_hash": plan_hash,
            "status": "pending",
            "created_at": datetime.now(UTC).isoformat(),
            "decided_at": None,
            "decided_by": None,
            "decision_note": None,
        }
        approvals.append(record)
        write_json(self.path, approvals)
        return record

    def decide(
        self,
        approval_id: str,
        status: str,
        decided_by: str,
        decision_note: str = "",
    ) -> dict[str, Any]:
        if status not in {"approved", "rejected"}:
            raise ValueError("approval status must be approved or rejected")
        approvals = self.list()
        for item in approvals:
            if item["approval_id"] == approval_id:
                if item["status"] != "pending":
                    raise ValueError("approval is not pending")
                item["status"] = status
                item["decided_at"] = datetime.now(UTC).isoformat()
                item["decided_by"] = decided_by
                item["decision_note"] = decision_note
                write_json(self.path, approvals)
                return item
        raise KeyError(f"approval not found: {approval_id}")

    def approved_for(self, request_id: str, plan_hash: str) -> bool:
        return any(
            item["request_id"] == request_id
            and item["plan_hash"] == plan_hash
            and item["status"] == "approved"
            for item in self.list()
        )

    def list(self, tenant: str | None = None) -> list[dict[str, Any]]:
        approvals = read_json(self.path, [])
        if tenant is None:
            return approvals
        return [item for item in approvals if item.get("tenant") == tenant]
