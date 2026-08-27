from __future__ import annotations

import os
import tempfile
import unittest

from enterprise_orchestrator.appliance_api.operations import (
    create_backup,
    list_updates,
    stage_update,
)
from enterprise_orchestrator.eaap_integration import ControlPlaneClient
from enterprise_orchestrator.evidence_service import EvidenceStore
from enterprise_orchestrator.execution_gateway.connectors import ReadOnlyDiagnosticConnector
from enterprise_orchestrator.governance_engine import GovernanceEvaluator
from enterprise_orchestrator.identity_service import IdentityService
from enterprise_orchestrator.llm_adapter.client import _load_json_response


class MaturityServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["EOA_STATE_DIR"] = self.temp_dir.name

    def tearDown(self) -> None:
        os.environ.pop("EOA_STATE_DIR", None)
        self.temp_dir.cleanup()

    def test_governance_evaluator_blocks_unapproved_tier_one_action(self) -> None:
        plan = {
            "domains": ["rhel"],
            "risk_tier": "T1",
            "confidence": "Medium",
            "recommended_actions": [
                {
                    "description": "Restart a service.",
                    "risk_tier": "T1",
                    "requires_approval": False,
                }
            ],
            "rollback": ["Start the service."],
            "validation": ["Check service status."],
            "governance": {"direct_impact": True, "notes": ["Access control affected."]},
        }

        result = GovernanceEvaluator().evaluate(plan)

        self.assertFalse(result.passed)
        self.assertIn("GR-004_APPROVAL_FLAG_REQUIRED", result.blocking_findings)

    def test_evidence_search_returns_matching_records(self) -> None:
        store = EvidenceStore()
        match = store.add("lab", "ncc", "Nutanix storage latency", "latency exceeded")
        store.add("lab", "auth", "Kerberos notes", "time drift")

        results = store.search("lab", "storage latency")

        self.assertEqual(results[0]["evidence_id"], match["evidence_id"])
        self.assertTrue(store.verify(match))
        self.assertTrue(store.verify_all("lab")["valid"])

    def test_semantic_evidence_search_scores_related_records(self) -> None:
        store = EvidenceStore()
        match = store.add("lab", "ncc", "Storage latency", "disk latency and iops")
        store.add("lab", "auth", "Kerberos notes", "time drift")

        results = store.semantic_search("lab", "storage iops latency")

        self.assertEqual(results[0]["evidence_id"], match["evidence_id"])
        self.assertGreater(results[0]["similarity"], 0)

    def test_evidence_signature_detects_content_tampering(self) -> None:
        store = EvidenceStore()
        record = store.add("lab", "source", "summary", "original")
        record["content"] = "changed"

        self.assertFalse(store.verify(record))

    def test_identity_rbac_defaults_to_fail_closed_for_unknown_actor(self) -> None:
        identity = IdentityService()

        self.assertTrue(identity.can("operator@example.local", "update:stage", "lab"))
        self.assertFalse(identity.can("anonymous@example.local", "request:create", "lab"))

    def test_identity_rbac_respects_tenant_scope(self) -> None:
        identity = IdentityService()
        identity.upsert_user("approver@example.local", "approver", tenants=["lab"])

        self.assertTrue(identity.can("approver@example.local", "approval:decide", "lab"))
        self.assertFalse(identity.can("approver@example.local", "approval:decide", "prod"))

    def test_eaap_client_is_disabled_until_configured(self) -> None:
        client = ControlPlaneClient(base_url="")

        self.assertFalse(client.status()["configured"])
        with self.assertRaises(RuntimeError):
            client.handoff_plan({"request_id": "req-test"})

    def test_connector_catalogue_only_plans_commands(self) -> None:
        connector = ReadOnlyDiagnosticConnector()

        self.assertFalse(connector.capabilities()["executes_commands"])
        commands = connector.plan(["nutanix"])
        self.assertTrue(commands)
        self.assertIn("command", commands[0])

    def test_update_staging_never_enables_apply(self) -> None:
        update = stage_update(
            artifact_path="internal/release.tar.gz",
            sha256="abc123",
            requested_by="operator",
            version="0.3.0",
        )

        self.assertFalse(update["apply_enabled"])
        self.assertEqual(list_updates()[0]["status"], "staged")

    def test_backup_creates_archive(self) -> None:
        EvidenceStore().add("lab", "source", "summary", "content")

        backup = create_backup()

        self.assertTrue(backup["path"].endswith(".tar.gz"))

    def test_ollama_response_json_repair_extracts_object(self) -> None:
        repaired = _load_json_response('prefix {"summary": "ok"} suffix')

        self.assertEqual(repaired["summary"], "ok")


if __name__ == "__main__":
    unittest.main()
