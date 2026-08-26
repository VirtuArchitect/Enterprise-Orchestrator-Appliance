from __future__ import annotations

import copy
import unittest

from enterprise_orchestrator.orchestrator_api import (
    ContractValidationError,
    OrchestrationRequest,
    submit_plan,
    validate_model_output,
)
from enterprise_orchestrator.orchestrator_api.models import RiskTier


def valid_plan() -> dict[str, object]:
    return {
        "summary": "Collect cluster health evidence before recommending changes.",
        "known": ["Operator reports degraded VM performance."],
        "missing": ["Cluster health output", "Storage latency metrics"],
        "required": ["ncli cluster get-domain-fault-tolerance-status"],
        "domains": ["nutanix", "storage"],
        "risk_tier": "T0",
        "confidence": "Medium",
        "recommended_actions": [
            {
                "description": "Collect read-only cluster and storage health output.",
                "risk_tier": "T0",
                "requires_approval": False,
            }
        ],
        "validation": ["Confirm health output was collected with timestamps."],
        "rollback": [],
        "governance": {
            "direct_impact": False,
            "notes": ["No direct governance impact for read-only evidence collection."],
        },
    }


class ContractValidationTests(unittest.TestCase):
    def test_accepts_valid_contract(self) -> None:
        validate_model_output(valid_plan())

    def test_rejects_missing_required_field(self) -> None:
        plan = valid_plan()
        del plan["confidence"]

        with self.assertRaisesRegex(ContractValidationError, "confidence"):
            validate_model_output(plan)

    def test_rejects_additional_fields(self) -> None:
        plan = valid_plan()
        plan["unreviewed_field"] = "model drift"

        with self.assertRaisesRegex(ContractValidationError, "additional"):
            validate_model_output(plan)

    def test_rejects_invalid_risk_tier(self) -> None:
        plan = valid_plan()
        plan["risk_tier"] = "T4"

        with self.assertRaisesRegex(ContractValidationError, "expected one of"):
            validate_model_output(plan)


class OrchestrationDecisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = OrchestrationRequest(
            request_id="req-001",
            submitted_by="operator@example.local",
            tenant="lab",
            task="Troubleshoot degraded Nutanix VM performance.",
        )

    def test_t0_plan_is_ready_without_approval(self) -> None:
        envelope = submit_plan(self.request, valid_plan())

        self.assertEqual(envelope["status"], "ready_for_t0_execution")
        decision = envelope["governance_decision"]
        self.assertEqual(decision["risk_tier"], "T0")
        self.assertFalse(decision["requires_approval"])
        self.assertEqual(decision["blockers"], [])

    def test_low_confidence_plan_requests_evidence(self) -> None:
        plan = valid_plan()
        plan["confidence"] = "Low"

        envelope = submit_plan(self.request, plan)

        self.assertEqual(envelope["status"], "needs_evidence")
        decision = envelope["governance_decision"]
        self.assertIn("LOW_CONFIDENCE_REQUIRES_MORE_EVIDENCE", decision["blockers"])
        self.assertTrue(decision["next_validation_steps"])

    def test_t1_plan_routes_to_approval(self) -> None:
        plan = valid_plan()
        plan["risk_tier"] = "T1"
        plan["recommended_actions"] = [
            {
                "description": "Restart a non-critical local service after approval.",
                "risk_tier": "T1",
                "requires_approval": True,
            }
        ]
        plan["rollback"] = ["Start the service again if the restart leaves it stopped."]

        envelope = submit_plan(self.request, plan)

        self.assertEqual(envelope["status"], "ready_for_approval")
        decision = envelope["governance_decision"]
        self.assertTrue(decision["requires_approval"])
        self.assertEqual(decision["risk_tier"], "T1")

    def test_request_boundary_can_raise_plan_tier(self) -> None:
        request = OrchestrationRequest(
            request_id="req-002",
            submitted_by="operator@example.local",
            task="Prepare for a disruptive operation.",
            requested_action_boundary=RiskTier.T2,
        )
        plan = valid_plan()
        plan["rollback"] = ["Do not execute; return to read-only checks."]

        envelope = submit_plan(request, plan)

        self.assertEqual(envelope["status"], "ready_for_approval")
        self.assertEqual(envelope["governance_decision"]["risk_tier"], "T2")

    def test_disruptive_plan_without_rollback_is_blocked(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["risk_tier"] = "T2"
        plan["recommended_actions"] = [
            {
                "description": "Reboot a node.",
                "risk_tier": "T2",
                "requires_approval": True,
            }
        ]
        plan["rollback"] = []

        envelope = submit_plan(self.request, plan)

        self.assertEqual(envelope["status"], "needs_evidence")
        self.assertIn(
            "DISRUPTIVE_ACTION_REQUIRES_ROLLBACK",
            envelope["governance_decision"]["blockers"],
        )


if __name__ == "__main__":
    unittest.main()
