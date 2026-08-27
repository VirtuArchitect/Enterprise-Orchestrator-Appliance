from __future__ import annotations

from pathlib import Path
import hashlib
from typing import Any

from enterprise_orchestrator.appliance_api import appliance_status
from enterprise_orchestrator.eaap_integration import ControlPlaneClient
from enterprise_orchestrator.evidence_service import EvidenceStore


ROOT = Path(__file__).resolve().parents[2]


def create_app() -> Any:
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise RuntimeError(
            "FastAPI runtime is optional. Install with "
            "`pip install .[api]` to use enterprise_orchestrator.fastapi_app`."
        ) from exc

    app = FastAPI(
        title="Enterprise Orchestrator Appliance API",
        version=(ROOT / "VERSION").read_text(encoding="utf-8").strip(),
    )

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return appliance_status(ROOT)

    @app.get("/api/evidence")
    def evidence(tenant: str | None = None) -> dict[str, Any]:
        return {"evidence": EvidenceStore().list(tenant=tenant)}

    @app.get("/api/evidence/verify")
    def verify_evidence(tenant: str | None = None) -> dict[str, Any]:
        return EvidenceStore().verify_all(tenant=tenant)

    @app.get("/api/evidence/semantic-search")
    def semantic_search(tenant: str, q: str) -> dict[str, Any]:
        return {"evidence": EvidenceStore().semantic_search(tenant=tenant, query=q)}

    @app.get("/api/integrations/eaap")
    def eaap_status() -> dict[str, Any]:
        return ControlPlaneClient().status()

    @app.get("/api/prompt-policy")
    def prompt_policy() -> dict[str, Any]:
        prompt = (ROOT / "prompts" / "enterprise-orchestrator-v5.6.md").read_text(
            encoding="utf-8"
        )
        return {
            "status": "production-oriented policy pack",
            "path": "prompts/enterprise-orchestrator-v5.6.md",
            "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        }

    @app.get("/api/release/status")
    def release_status() -> dict[str, Any]:
        return {
            "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            "demo_url": (ROOT / "DEMO_URL").read_text(encoding="utf-8").strip(),
            "demo_status": (ROOT / "DEMO_STATUS").read_text(encoding="utf-8").strip(),
            "fastapi_runtime": "optional",
            "appliance_image": "planned_not_validated",
        }

    return app


try:
    app = create_app()
except RuntimeError:
    app = None
