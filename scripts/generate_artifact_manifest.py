from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUDES = {
    ".git",
    ".local-state",
    ".local-state-dev",
    "__pycache__",
    ".pytest_cache",
    "dist",
}


def main() -> None:
    output = ROOT / "deployments" / "appliance" / "artifact-manifest.json"
    records = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or _excluded(path):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative == output.relative_to(ROOT).as_posix():
            continue
        records.append(
            {
                "path": relative,
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "artifact": "enterprise-orchestrator-appliance-source",
        "files": records,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)} with {len(records)} files.")


def _excluded(path: Path) -> bool:
    return any(part in DEFAULT_EXCLUDES for part in path.relative_to(ROOT).parts)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    main()
