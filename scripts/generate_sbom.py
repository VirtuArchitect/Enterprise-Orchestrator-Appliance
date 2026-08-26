from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    output = ROOT / "deployments" / "appliance" / "sbom.json"
    payload = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(UTC).isoformat(),
            "component": {
                "type": "application",
                "name": "enterprise-orchestrator-appliance",
                "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            },
        },
        "components": [
            {
                "type": "container",
                "name": "python",
                "version": "3.12.7-slim",
                "purl": "pkg:docker/python@3.12.7-slim",
                "hashes": [
                    {
                        "alg": "SHA-256",
                        "content": "60d9996b6a8a3689d36db740b49f4327be3be09a21122bd02fb8895abb38b50d",
                    }
                ],
            },
            {
                "type": "library",
                "name": "python-standard-library",
                "version": "3.12",
                "scope": "required",
            },
        ],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
