from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build_plan() -> dict[str, object]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "artifact": "enterprise-orchestrator-appliance-image-plan",
        "status": "plan_only",
        "target": "Nutanix AHV / RHEL compatible VM image",
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
        "non_claim": "This plan does not produce or validate a QCOW2 image.",
    }


def main() -> None:
    output = ROOT / "deployments" / "appliance" / "image-build-plan.json"
    output.write_text(json.dumps(build_plan(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
