from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class PhaseTwentyTwoToTwentyEightStaticTests(unittest.TestCase):
    def test_release_gates_validate_without_regenerating_artifacts(self) -> None:
        release_gates = (REPO_ROOT / "scripts" / "run_release_gates.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("scripts/validate_release_artifacts.py", release_gates)
        self.assertNotIn("scripts/generate_sbom.py", release_gates)
        self.assertNotIn("scripts/generate_artifact_manifest.py", release_gates)
        self.assertNotIn("scripts/plan_appliance_image.py", release_gates)

    def test_phase_22_28_files_are_present(self) -> None:
        required = [
            "scripts/generate_release_artifacts.py",
            "scripts/validate_release_artifacts.py",
            "scripts/validate_eaap_integration_config.py",
            "scripts/build_appliance_image.py",
            "src/enterprise_orchestrator/conversation_service/store.py",
            "src/enterprise_orchestrator/evidence_service/attachments.py",
            "src/enterprise_orchestrator/appliance_api/settings.py",
            "src/enterprise_orchestrator/identity_service/adapters.py",
            "docs/operations/identity-adapter.md",
            "docs/operations/eaap-integration.md",
            "docs/operations/image-build-evidence-template.md",
        ]

        for relative in required:
            self.assertTrue((REPO_ROOT / relative).exists(), relative)

    def test_console_exposes_phase_22_28_controls(self) -> None:
        index = (REPO_ROOT / "ui" / "index.html").read_text(encoding="utf-8")
        app = (REPO_ROOT / "ui" / "app.js").read_text(encoding="utf-8")

        for control in (
            "newConversation",
            "uploadAttachment",
            "adminSettings",
            "identityStatus",
            "eaapValidation",
        ):
            self.assertIn(control, index)
        for endpoint in (
            "/api/conversations",
            "/api/evidence/attachments",
            "/api/admin/settings",
            "/api/identity/status",
            "/api/integrations/eaap/validation-plan",
        ):
            self.assertIn(endpoint, app)

    def test_image_build_script_is_plan_only_by_default(self) -> None:
        script = (REPO_ROOT / "scripts" / "build_appliance_image.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("EOA_IMAGE_BUILD_MODE", script)
        self.assertIn("plan-only", script)
        self.assertIn("intentionally unimplemented", script)


if __name__ == "__main__":
    unittest.main()
