from __future__ import annotations

import json

from enterprise_orchestrator.eaap_integration import ControlPlaneClient


def main() -> None:
    client = ControlPlaneClient()
    plan = client.validation_plan()
    print(json.dumps(plan, indent=2, sort_keys=True))
    if not plan["configured"]:
        print("EAAP integration validation skipped: EOA_EAAP_CONTROL_PLANE_URL is not set.")
        return
    status = client.status()
    if status["boundary"] != "plan_handoff_only":
        raise SystemExit("FAIL: EAAP integration is not limited to plan handoff")
    print("EAAP integration configuration validation passed.")


if __name__ == "__main__":
    main()
