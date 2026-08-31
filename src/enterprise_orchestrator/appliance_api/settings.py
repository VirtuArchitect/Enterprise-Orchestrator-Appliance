from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from enterprise_orchestrator.appliance_api import appliance_status
from enterprise_orchestrator.eaap_integration import ControlPlaneClient
from enterprise_orchestrator.identity_service.adapters import identity_adapter_status


def admin_settings(root: Path) -> dict[str, Any]:
    status = appliance_status(root)
    return {
        "version": status["version"],
        "demo": {
            "url": _optional_file(root, "DEMO_URL"),
            "status": _optional_file(root, "DEMO_STATUS"),
        },
        "runtime": {
            "llm_provider": status["runtime"]["llm_provider"],
            "model": status["runtime"]["model"],
            "fastapi": "optional",
        },
        "identity": identity_adapter_status(),
        "eaap_integration": ControlPlaneClient().status(),
        "execution": {
            "live_mutation_enabled": False,
            "dry_run_gateway_enabled": True,
            "approval_required_for_t1_plus": True,
        },
        "updates": {
            "stage_enabled": True,
            "apply_enabled": False,
        },
        "release": {
            "gate_command": "PYTHONPATH=src python scripts/run_release_gates.py",
            "regenerate_command": "PYTHONPATH=src python scripts/generate_release_artifacts.py",
            "public_demo_source": "docs/demo/index.html",
        },
        "state_dir": os.environ.get("EOA_STATE_DIR") or ".local-state",
    }


def _optional_file(root: Path, name: str) -> str:
    path = root / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()
