from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from enterprise_orchestrator.approval_workflow import ApprovalQueue
from enterprise_orchestrator.audit_service import AuditStore
from enterprise_orchestrator.evidence_service import EvidenceStore
from enterprise_orchestrator.execution_gateway import DryRunExecutionGateway


class ServiceStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["EOA_STATE_DIR"] = self.temp_dir.name

    def tearDown(self) -> None:
        os.environ.pop("EOA_STATE_DIR", None)
        self.temp_dir.cleanup()

    def test_evidence_store_filters_by_tenant(self) -> None:
        store = EvidenceStore()
        first = store.add("tenant-a", "log", "A log", "content")
        store.add("tenant-b", "log", "B log", "content")

        self.assertEqual(store.list("tenant-a"), [first])
        self.assertEqual(store.get_many([first["evidence_id"]], "tenant-a"), [first])

    def test_audit_store_builds_and_verifies_chain(self) -> None:
        store = AuditStore()
        store.append("request.created", "tenant-a", "operator", {"request_id": "req-1"})
        store.append("plan.generated", "tenant-a", "operator", {"request_id": "req-1"})

        self.assertTrue(store.verify_chain())
        self.assertEqual(len(store.list("tenant-a")), 2)

    def test_audit_chain_detects_tampering(self) -> None:
        store = AuditStore()
        store.append("request.created", "tenant-a", "operator", {"request_id": "req-1"})
        path = Path(os.environ["EOA_STATE_DIR"]) / "audit.jsonl"
        contents = path.read_text(encoding="utf-8")
        path.write_text(contents.replace("req-1", "req-2"), encoding="utf-8")

        self.assertFalse(store.verify_chain())

    def test_approval_queue_is_plan_hash_bound(self) -> None:
        queue = ApprovalQueue()
        approval = queue.create("req-1", "tenant-a", "operator", "T1", "Needs approval", "abc")

        self.assertFalse(queue.approved_for("req-1", "abc"))
        queue.decide(approval["approval_id"], "approved", "approver")
        self.assertTrue(queue.approved_for("req-1", "abc"))
        self.assertFalse(queue.approved_for("req-1", "def"))

    def test_dry_run_gateway_blocks_non_dry_run_mode(self) -> None:
        gateway = DryRunExecutionGateway()
        with self.assertRaises(PermissionError):
            gateway.execute(
                "req-1",
                "tenant-a",
                "operator",
                {"risk_tier": "T0", "recommended_actions": []},
                approved=False,
                mode="apply",
            )

    def test_dry_run_gateway_requires_approval_for_tier_one(self) -> None:
        gateway = DryRunExecutionGateway()
        with self.assertRaises(PermissionError):
            gateway.execute(
                "req-1",
                "tenant-a",
                "operator",
                {"risk_tier": "T1", "recommended_actions": []},
                approved=False,
            )

        result = gateway.execute(
            "req-1",
            "tenant-a",
            "operator",
            {"risk_tier": "T1", "recommended_actions": []},
            approved=True,
        )
        self.assertEqual(result["status"], "completed")


if __name__ == "__main__":
    unittest.main()
