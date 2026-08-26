from __future__ import annotations

import tarfile
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "dist"
INCLUDED_FILES = [
    "README.md",
    "STATUS.md",
    "docs/architecture/overview.md",
    "docs/architecture/deployment.md",
    "docs/operations/local-development.md",
    "docs/operations/appliance-update-boundary.md",
    "deployments/docker/compose.yaml",
    "deployments/docker/compose.ollama.yaml",
    "deployments/appliance/artifact-manifest.json",
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    bundle = OUTPUT_DIR / f"enterprise-orchestrator-support-bundle-{stamp}.tar.gz"
    with tarfile.open(bundle, "w:gz") as archive:
        for relative in INCLUDED_FILES:
            path = ROOT / relative
            if path.exists():
                archive.add(path, arcname=relative)
    print(f"Wrote {bundle}")


if __name__ == "__main__":
    main()
