from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATE_DIR = ROOT / ".local-state"


def state_dir() -> Path:
    configured = os.environ.get("EOA_STATE_DIR")
    return Path(configured).expanduser().resolve() if configured else DEFAULT_STATE_DIR


def ensure_state_dir() -> Path:
    path = state_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path
