from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class OperatorUiStaticTests(unittest.TestCase):
    def test_console_defaults_to_light_with_dark_mode_toggle(self) -> None:
        index = (REPO_ROOT / "ui" / "index.html").read_text(encoding="utf-8")
        styles = (REPO_ROOT / "ui" / "styles.css").read_text(encoding="utf-8")
        app = (REPO_ROOT / "ui" / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="themeToggle"', index)
        self.assertIn("color-scheme: light", styles)
        self.assertIn(':root[data-theme="dark"]', styles)
        self.assertIn("enterprise-orchestrator-theme", app)
        self.assertIn('applyTheme(localStorage.getItem(THEME_KEY) || "light")', app)


if __name__ == "__main__":
    unittest.main()
