from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class PhaseTenToFifteenStaticTests(unittest.TestCase):
    def test_fastapi_runtime_is_optional_extra(self) -> None:
        pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        fastapi_app = (
            REPO_ROOT / "src" / "enterprise_orchestrator" / "fastapi_app.py"
        ).read_text(encoding="utf-8")

        self.assertIn("[project.optional-dependencies]", pyproject)
        self.assertIn("fastapi", pyproject)
        self.assertIn("def create_app()", fastapi_app)

    def test_release_gate_and_image_plan_are_documented(self) -> None:
        status = (REPO_ROOT / "STATUS.md").read_text(encoding="utf-8")
        release_gates = (REPO_ROOT / "scripts" / "run_release_gates.py").read_text(
            encoding="utf-8"
        )
        image_plan = (REPO_ROOT / "scripts" / "plan_appliance_image.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("Phase 10-15 implementation", status)
        self.assertIn("Release gates passed", release_gates)
        self.assertIn("plan_only", image_plan)

    def test_demo_url_is_release_managed(self) -> None:
        demo_url = (REPO_ROOT / "DEMO_URL").read_text(encoding="utf-8").strip()
        demo_status = (REPO_ROOT / "DEMO_STATUS").read_text(encoding="utf-8").strip()
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        release_notes = (REPO_ROOT / "docs" / "release" / "RELEASE_NOTES.md").read_text(
            encoding="utf-8"
        )
        demo_page = (REPO_ROOT / "docs" / "demo" / "index.html").read_text(
            encoding="utf-8"
        )

        self.assertEqual(
            demo_url,
            "https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/",
        )
        self.assertIn(
            demo_status,
            {"pending-pages-deployment", "pending-github-pages-support", "live"},
        )
        self.assertIn(demo_url, readme)
        self.assertIn(demo_url, release_notes)
        self.assertIn(demo_status, readme)
        self.assertIn(demo_status, release_notes)
        self.assertIn("v0.4.0 demo", demo_page)

    def test_prompt_policy_contains_governed_clauses(self) -> None:
        prompt = (
            REPO_ROOT / "prompts" / "enterprise-orchestrator-v5.6.md"
        ).read_text(encoding="utf-8")
        required = [
            "Evidence first",
            "Contract first",
            "Governance first",
            "Fail closed",
            "No invention",
            "No secrets",
            "No direct mutation",
            "T0 read-only",
            "T3 destructive",
        ]

        for clause in required:
            self.assertIn(clause, prompt)

    def test_console_exposes_policy_and_integration_controls(self) -> None:
        index = (REPO_ROOT / "ui" / "index.html").read_text(encoding="utf-8")
        app = (REPO_ROOT / "ui" / "app.js").read_text(encoding="utf-8")

        for control in (
            "semanticSearch",
            "verifyEvidence",
            "promptPolicy",
            "releaseStatus",
            "eaapStatus",
        ):
            self.assertIn(control, index)
        self.assertIn("#settings", index)
        self.assertIn("#about", index)
        self.assertIn("/api/prompt-policy", app)
        self.assertIn("/api/release/status", app)
        self.assertIn("/api/integrations/eaap", app)


if __name__ == "__main__":
    unittest.main()
