from __future__ import annotations

import os
from typing import Any


SUPPORTED_MODES = {"local-bootstrap", "oidc-planned", "saml-planned"}


def identity_adapter_status() -> dict[str, Any]:
    mode = os.environ.get("EOA_IDENTITY_MODE", "local-bootstrap").strip() or "local-bootstrap"
    configured = bool(os.environ.get("EOA_IDENTITY_ISSUER_URL"))
    if mode not in SUPPORTED_MODES:
        return {
            "mode": mode,
            "configured": False,
            "valid": False,
            "boundary": "unsupported_identity_mode",
            "supported_modes": sorted(SUPPORTED_MODES),
        }
    return {
        "mode": mode,
        "configured": configured,
        "valid": mode == "local-bootstrap" or configured,
        "boundary": (
            "local_bootstrap_only"
            if mode == "local-bootstrap"
            else "enterprise_identity_adapter_declared_not_enforced"
        ),
        "supported_modes": sorted(SUPPORTED_MODES),
    }
