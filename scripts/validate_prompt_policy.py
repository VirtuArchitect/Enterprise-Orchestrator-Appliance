from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "prompts" / "enterprise-orchestrator-v5.6.md"
REQUIRED_CLAUSES = [
    "Evidence first",
    "Contract first",
    "Governance first",
    "Fail closed",
    "Least authority",
    "No invention",
    "No secrets",
    "No direct mutation",
    "T0 read-only",
    "T1 low-risk reversible",
    "T2 disruptive",
    "T3 destructive",
    "Return one JSON object",
]


def main() -> None:
    text = PROMPT.read_text(encoding="utf-8")
    missing = [clause for clause in REQUIRED_CLAUSES if clause not in text]
    if missing:
        raise SystemExit("prompt policy missing clauses: " + ", ".join(missing))
    print("Prompt policy validation passed.")


if __name__ == "__main__":
    main()
