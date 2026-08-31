from __future__ import annotations

from generate_artifact_manifest import main as generate_manifest
from generate_sbom import main as generate_sbom
from plan_appliance_image import main as generate_image_plan


def main() -> None:
    generate_sbom()
    generate_image_plan()
    generate_manifest()
    print("Release artifacts regenerated.")


if __name__ == "__main__":
    main()
