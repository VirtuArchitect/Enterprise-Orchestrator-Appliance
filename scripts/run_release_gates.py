from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


COMMANDS = [
    [sys.executable, "scripts/generate_sbom.py"],
    [sys.executable, "scripts/plan_appliance_image.py"],
    [sys.executable, "scripts/generate_artifact_manifest.py"],
    [sys.executable, "scripts/validate_repository.py"],
    [sys.executable, "scripts/validate_demo_link.py"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
    [sys.executable, "scripts/smoke_app.py"],
    [sys.executable, "scripts/scan_public_hygiene.py"],
    ["docker", "compose", "-f", "deployments/docker/compose.yaml", "config"],
    [
        "docker",
        "compose",
        "-f",
        "deployments/docker/compose.yaml",
        "-f",
        "deployments/docker/compose.ollama.yaml",
        "config",
    ],
    ["git", "diff", "--check"],
]


def main() -> None:
    for command in COMMANDS:
        print("+ " + " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    print("Release gates passed.")


if __name__ == "__main__":
    main()
