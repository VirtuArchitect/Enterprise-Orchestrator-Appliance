from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build_plan(timestamp: str | None = None) -> dict[str, object]:
    return {
        "generated_at": timestamp or os.environ.get("EOA_RELEASE_TIMESTAMP") or datetime.now(UTC).isoformat(),
        "artifact": "enterprise-orchestrator-appliance-image-plan",
        "status": "plan_only",
        "target": "Nutanix AHV / RHEL compatible VM image",
        "build_script": "scripts/build_appliance_image.py",
        "evidence_template": "docs/operations/image-build-evidence-template.md",
        "required_inputs": [
            "RHEL installation media or approved golden image",
            "offline Python runtime and optional FastAPI wheelhouse",
            "local model runtime bundle or approved Ollama model cache",
            "signed source release artifact and artifact-manifest.json",
        ],
        "phases": [
            "install base OS",
            "create enterprise-orchestrator service account",
            "install source under /opt/enterprise-orchestrator",
            "seed /var/lib/enterprise-orchestrator with empty state",
            "install and enable enterprise-orchestrator.service",
            "run firstboot.sh",
            "capture image",
            "boot cloned image and run smoke_app.py",
        ],
        "validation": [
            "run scripts/build_appliance_image.py in default plan mode",
            "run scripts/validate_release_artifacts.py",
            "capture offline artifact checksums before transfer",
            "boot cloned image and run smoke_app.py",
        ],
        "non_claim": "This plan does not produce or validate a QCOW2 image.",
    }


def main() -> None:
    output = ROOT / "deployments" / "appliance" / "image-build-plan.json"
    output.write_text(json.dumps(build_plan(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
