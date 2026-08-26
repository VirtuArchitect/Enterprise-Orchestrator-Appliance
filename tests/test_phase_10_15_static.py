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
        self.assertIn("v0.2.0 demo", demo_page)


if __name__ == "__main__":
    unittest.main()
