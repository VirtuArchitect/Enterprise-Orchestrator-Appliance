from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from enterprise_orchestrator.paths import ensure_state_dir


def appliance_status(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    state = ensure_state_dir()
    ollama_url = os.environ.get("EOA_OLLAMA_URL", "")
    return {
        "status": "healthy",
        "version": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "runtime": {
            "llm_provider": "ollama" if ollama_url else "deterministic",
            "ollama_configured": bool(ollama_url),
            "model": os.environ.get("EOA_OLLAMA_MODEL", "llama3:8b"),
        },
        "paths": {
            "root": str(root),
            "state_dir": str(state),
        },
        "capabilities": {
            "contract_validation": True,
            "operator_ui": True,
            "evidence_store": True,
            "evidence_signing": True,
            "semantic_evidence_search": True,
            "approval_queue": True,
            "local_rbac": True,
            "fastapi_runtime_optional": True,
            "eaap_control_plane_handoff": bool(os.environ.get("EOA_EAAP_CONTROL_PLANE_URL", "")),
            "audit_chain": True,
            "dry_run_execution": True,
            "read_only_connector_plan": True,
            "backup_create": True,
            "support_bundle_export": True,
            "release_gate_script": True,
            "appliance_image_plan": True,
            "update_stage": True,
            "live_execution": False,
            "appliance_update_apply": False,
        },
    }
