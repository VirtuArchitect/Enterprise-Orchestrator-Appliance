from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "STATUS.md",
    "VERSION",
    "DEMO_URL",
    "CHANGELOG.md",
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
    "pyproject.toml",
    "src/enterprise_orchestrator/__init__.py",
    "src/enterprise_orchestrator/orchestrator_api/__init__.py",
    "src/enterprise_orchestrator/orchestrator_api/contract.py",
    "src/enterprise_orchestrator/orchestrator_api/models.py",
    "src/enterprise_orchestrator/orchestrator_api/service.py",
    "src/enterprise_orchestrator/llm_adapter/client.py",
    "src/enterprise_orchestrator/evidence_service/store.py",
    "src/enterprise_orchestrator/identity_service/rbac.py",
    "src/enterprise_orchestrator/eaap_integration/client.py",
    "src/enterprise_orchestrator/audit_service/store.py",
    "src/enterprise_orchestrator/approval_workflow/queue.py",
    "src/enterprise_orchestrator/execution_gateway/dry_run.py",
    "src/enterprise_orchestrator/execution_gateway/connectors.py",
    "src/enterprise_orchestrator/governance_engine/rules.py",
    "src/enterprise_orchestrator/appliance_api/status.py",
    "src/enterprise_orchestrator/appliance_api/operations.py",
    "src/enterprise_orchestrator/app.py",
    "src/enterprise_orchestrator/fastapi_app.py",
    "tests/test_orchestrator_api.py",
    "tests/test_llm_adapter.py",
    "tests/test_services.py",
    "tests/test_maturity_services.py",
    "scripts/smoke_app.py",
    "scripts/generate_artifact_manifest.py",
    "scripts/create_support_bundle.py",
    "scripts/generate_sbom.py",
    "scripts/plan_appliance_image.py",
    "scripts/run_release_gates.py",
    "scripts/scan_public_hygiene.py",
    "scripts/validate_demo_link.py",
    "ui/index.html",
    "ui/styles.css",
    "ui/app.js",
    "docs/demo/index.html",
    "deployments/docker/Dockerfile",
    "deployments/docker/compose.yaml",
    "deployments/docker/compose.ollama.yaml",
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
    "deployments/appliance/firstboot.sh",
    "deployments/appliance/enterprise-orchestrator.service",
    "deployments/appliance/artifact-manifest.json",
    "deployments/appliance/sbom.json",
    "deployments/appliance/image-build-plan.json",
    "docs/operations/local-development.md",
    "docs/operations/appliance-update-boundary.md",
    "docs/operations/ahv-rhel-appliance.md",
    "docs/operations/phase-10-15-implementation.md",
    "docs/release/RELEASE_NOTES.md",
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
