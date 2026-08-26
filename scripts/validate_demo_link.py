from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_REQUIRED = [
    "README.md",
    "CHANGELOG.md",
    "docs/release/RELEASE_NOTES.md",
    "docs/demo/index.html",
]


def main() -> None:
    demo_url = (ROOT / "DEMO_URL").read_text(encoding="utf-8").strip()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not demo_url.startswith("https://"):
        raise SystemExit("DEMO_URL must be an https URL")
    missing = []
    for relative_path in DOCS_REQUIRED:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if demo_url not in text and relative_path != "docs/demo/index.html":
            missing.append(relative_path)
        if relative_path == "docs/demo/index.html" and version not in text:
            missing.append(f"{relative_path} missing version {version}")
    if missing:
        raise SystemExit("demo link validation failed: " + ", ".join(missing))
    print(f"Demo link validation passed: {demo_url}")


if __name__ == "__main__":
    main()
