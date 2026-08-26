from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "STATUS.md",
    "AGENTS.md",
    "TESTING_GUIDE.md",
    "SECURITY_REVIEW.md",
    "CODE_REVIEW.md",
    "docs/architecture/README.md",
    "docs/architecture/overview.md",
    "docs/architecture/data-flow.md",
    "docs/architecture/deployment.md",
    "docs/operations/README.md",
    "prompts/enterprise-orchestrator-v5.6.md",
    "prompts/output-contract.schema.json",
    "services/README.md",
    "services/orchestrator-api/README.md",
    "services/llm-adapter/README.md",
    "services/evidence-service/README.md",
    "services/audit-service/README.md",
    "services/appliance-api/README.md",
    "ui/README.md",
    "deployments/README.md",
    "deployments/docker/README.md",
    "deployments/appliance/README.md",
]

REQUIRED_README_PHRASES = [
    "Enterprise Orchestrator Appliance",
    "The LLM produces plans and recommendations",
    "production-ready autonomous infrastructure operator",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    missing = []
    empty = []
    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        if not path.exists():
            missing.append(relative_path)
        elif path.is_file() and path.stat().st_size == 0:
            empty.append(relative_path)

    if missing:
        fail("missing required files: " + ", ".join(missing))
    if empty:
        fail("empty required files: " + ", ".join(empty))

    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    absent_phrases = [
        phrase for phrase in REQUIRED_README_PHRASES if phrase.lower() not in readme
    ]
    if absent_phrases:
        fail("README missing expected phrases: " + ", ".join(absent_phrases))

    schema_path = ROOT / "prompts/output-contract.schema.json"
    with schema_path.open(encoding="utf-8") as handle:
        schema = json.load(handle)

    required_fields = set(schema.get("required", []))
    for field in ("summary", "risk_tier", "confidence", "recommended_actions"):
        if field not in required_fields:
            fail(f"output contract missing required field: {field}")

    print("Repository scaffold validation passed.")


if __name__ == "__main__":
    main()
