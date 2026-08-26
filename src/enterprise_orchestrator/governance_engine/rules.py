from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GovernanceEvaluation:
    passed: bool
    blocking_findings: tuple[str, ...]
    warnings: tuple[str, ...]
    applied_rules: tuple[str, ...]


class GovernanceEvaluator:
    """Minimal GR-style evaluator for the local appliance MVP."""

    def evaluate(self, plan: dict[str, Any]) -> GovernanceEvaluation:
        blocking: list[str] = []
        warnings: list[str] = []
        applied = [
            "GR-001 governance before action",
            "GR-002 evidence classified",
            "GR-003 confidence quantified",
            "GR-004 approval above threshold",
            "GR-007 gateway-only execution",
            "GR-008 audit trail",
            "GR-009 rollback before execution",
        ]

        if plan.get("confidence") == "Low":
            blocking.append("GR-003_LOW_CONFIDENCE_BLOCKS_CONCLUSION")

        if not plan.get("domains"):
            blocking.append("GR-011_ACCOUNTABILITY_DOMAIN_REQUIRED")

        risk_tier = plan.get("risk_tier")
        if risk_tier in {"T2", "T3"}:
            if not plan.get("rollback"):
                blocking.append("GR-009_ROLLBACK_REQUIRED_FOR_DISRUPTIVE_ACTION")
            if not plan.get("validation"):
                blocking.append("GR-006_VALIDATION_REQUIRED_FOR_DISRUPTIVE_ACTION")

        for action in plan.get("recommended_actions", []):
            if action.get("risk_tier") in {"T1", "T2", "T3"} and not action.get(
                "requires_approval"
            ):
                blocking.append("GR-004_APPROVAL_FLAG_REQUIRED")

        if plan.get("governance", {}).get("direct_impact") and not plan.get(
            "governance", {}
        ).get("notes"):
            warnings.append("GOVERNANCE_IMPACT_NEEDS_MAPPING_NOTES")

        return GovernanceEvaluation(
            passed=not blocking,
            blocking_findings=tuple(blocking),
            warnings=tuple(warnings),
            applied_rules=tuple(applied),
        )
