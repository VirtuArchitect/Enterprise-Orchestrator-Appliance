from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


class ControlPlaneClient:
    def __init__(self, base_url: str | None = None, timeout: float = 5.0) -> None:
        self.base_url = (base_url or os.environ.get("EOA_EAAP_CONTROL_PLANE_URL", "")).rstrip("/")
        self.timeout = timeout

    def status(self) -> dict[str, Any]:
        return {
            "configured": bool(self.base_url),
            "base_url": self.base_url or None,
            "handoff_enabled": bool(self.base_url),
            "boundary": "disabled_fail_closed" if not self.base_url else "plan_handoff_only",
        }

    def validation_plan(self) -> dict[str, Any]:
        return {
            "configured": bool(self.base_url),
            "base_url": self.base_url or None,
            "required_endpoint": "/api/plan-handoffs",
            "required_contract": "governed request envelope with plan_hash",
            "validation_mode": "skipped_until_configured" if not self.base_url else "configured",
            "non_claim": "This validation path does not execute infrastructure mutation.",
        }

    def handoff_plan(self, envelope: dict[str, Any]) -> dict[str, Any]:
        if not self.base_url:
            raise RuntimeError("EAAP control-plane integration is not configured")
        request = Request(
            f"{self.base_url}/api/plan-handoffs",
            data=json.dumps({"request": envelope}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read().decode("utf-8")
        except URLError as exc:
            raise RuntimeError(f"EAAP handoff failed: {exc}") from exc
        return json.loads(payload or "{}")
