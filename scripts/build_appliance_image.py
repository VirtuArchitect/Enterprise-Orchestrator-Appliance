from __future__ import annotations

import json
import os
from pathlib import Path

from plan_appliance_image import build_plan


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_EXECUTE_ENV = [
    "EOA_RHEL_IMAGE",
    "EOA_OUTPUT_DIR",
]


def main() -> None:
    mode = os.environ.get("EOA_IMAGE_BUILD_MODE", "plan").strip().lower()
    plan = build_plan()
    if mode in {"", "plan", "validate"}:
        _validate_plan(plan)
        print(json.dumps({"mode": "plan", "status": "validated", "plan": plan}, indent=2))
        print("Appliance image build is plan-only; no image was created.")
        return
    if mode != "execute":
        raise SystemExit(f"FAIL: unsupported image build mode: {mode}")
    if os.environ.get("EOA_BUILDER_APPROVED") != "true":
        raise SystemExit("FAIL: image build execute mode requires EOA_BUILDER_APPROVED=true")
    missing = [name for name in REQUIRED_EXECUTE_ENV if not os.environ.get(name)]
    if missing:
        raise SystemExit("FAIL: missing image build inputs: " + ", ".join(missing))
    raise SystemExit(
        "FAIL: execute mode is intentionally unimplemented in this reference appliance. "
        "Use docs/operations/image-build-evidence-template.md for controlled build evidence."
    )


def _validate_plan(plan: dict[str, object]) -> None:
    if plan.get("status") != "plan_only":
        raise SystemExit("FAIL: appliance image plan must remain plan_only")
    if "non_claim" not in plan:
        raise SystemExit("FAIL: appliance image plan must include non_claim")


if __name__ == "__main__":
    main()
