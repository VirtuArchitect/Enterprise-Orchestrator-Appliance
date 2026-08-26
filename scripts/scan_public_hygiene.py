from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".local-state", ".local-state-dev", "dist", "__pycache__"}
PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]+"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"BEGIN (RSA|OPENSSH|PRIVATE) KEY"),
    re.compile(r"(?i)(password|secret|token)\s*=\s*[^\\s#]+"),
    re.compile(r"C:\\Users\\john", re.IGNORECASE),
]
ALLOWED_SNIPPETS = [
    "printf 'EOA_BOOTSTRAP_TOKEN='",
]


def main() -> None:
    findings: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".tar", ".gz"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(snippet in line for snippet in ALLOWED_SNIPPETS):
                continue
            if any(pattern.search(line) for pattern in PATTERNS):
                findings.append(f"{path.relative_to(ROOT)}:{line_number}")
    if findings:
        raise SystemExit("public hygiene scan found sensitive-looking content: " + ", ".join(findings))
    print("Public hygiene scan passed.")


if __name__ == "__main__":
    main()
