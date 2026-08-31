from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from generate_artifact_manifest import build_manifest
from generate_sbom import build_sbom
from plan_appliance_image import build_plan


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    _validate_json_artifact(
        ROOT / "deployments" / "appliance" / "sbom.json",
        "metadata.timestamp",
        lambda timestamp: build_sbom(timestamp=timestamp),
    )
    _validate_json_artifact(
        ROOT / "deployments" / "appliance" / "image-build-plan.json",
        "generated_at",
        lambda timestamp: build_plan(timestamp=timestamp),
    )
    _validate_json_artifact(
        ROOT / "deployments" / "appliance" / "artifact-manifest.json",
        "generated_at",
        lambda timestamp: build_manifest(timestamp=timestamp),
    )
    print("Release artifact validation passed.")


def _validate_json_artifact(
    path: Path,
    timestamp_field: str,
    builder: Any,
) -> None:
    if not path.exists():
        raise SystemExit(f"FAIL: missing release artifact: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as handle:
        actual = json.load(handle)
    timestamp = _field(actual, timestamp_field)
    expected = builder(timestamp)
    if actual != expected:
        raise SystemExit(f"FAIL: stale release artifact: {path.relative_to(ROOT)}")


def _field(payload: dict[str, Any], dotted_path: str) -> str:
    current: Any = payload
    for part in dotted_path.split("."):
        current = current[part]
    if not isinstance(current, str) or not current:
        raise SystemExit(f"FAIL: invalid timestamp field {dotted_path}")
    return current


if __name__ == "__main__":
    main()
