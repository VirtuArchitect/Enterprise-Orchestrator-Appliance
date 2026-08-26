from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


ROLE_PERMISSIONS = {
    "viewer": {
        "evidence:read",
        "request:read",
        "approval:read",
        "audit:read",
        "connector:plan",
    },
    "operator": {
        "evidence:create",
        "request:create",
        "execution:dry_run",
        "backup:create",
    },
    "approver": {
        "approval:decide",
    },
    "admin": {
        "update:stage",
        "identity:manage",
        "release:gate",
    },
}

ROLE_INHERITANCE = {
    "viewer": {"viewer"},
    "operator": {"viewer", "operator"},
    "approver": {"viewer", "operator", "approver"},
    "admin": {"viewer", "operator", "approver", "admin"},
}


class IdentityService:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ensure_state_dir() / "identity-users.json"
        self._ensure_bootstrap()

    def users(self) -> list[dict[str, Any]]:
        return read_json(self.path, [])

    def role_for(self, actor: str) -> str:
        actor = _normalize_actor(actor)
        for user in self.users():
            if _normalize_actor(user["actor"]) == actor and user.get("enabled", True):
                return user["role"]
        return "viewer"

    def can(self, actor: str, permission: str, tenant: str = "default") -> bool:
        role = self.role_for(actor)
        inherited_roles = ROLE_INHERITANCE.get(role, {"viewer"})
        allowed = set()
        for inherited_role in inherited_roles:
            allowed.update(ROLE_PERMISSIONS.get(inherited_role, set()))
        return permission in allowed and self._tenant_allowed(actor, tenant)

    def require(self, actor: str, permission: str, tenant: str = "default") -> None:
        if not self.can(actor, permission, tenant):
            role = self.role_for(actor)
            raise PermissionError(
                f"actor {actor!r} with role {role!r} lacks {permission!r}"
            )

    def upsert_user(
        self,
        actor: str,
        role: str,
        tenants: list[str] | None = None,
        enabled: bool = True,
    ) -> dict[str, Any]:
        if role not in ROLE_INHERITANCE:
            raise ValueError(f"unknown role: {role}")
        actor = _normalize_actor(actor)
        records = [user for user in self.users() if _normalize_actor(user["actor"]) != actor]
        record = {
            "actor": actor,
            "role": role,
            "tenants": tenants or ["*"],
            "enabled": enabled,
            "updated_at": datetime.now(UTC).isoformat(),
        }
        records.append(record)
        write_json(self.path, sorted(records, key=lambda user: user["actor"]))
        return record

    def _tenant_allowed(self, actor: str, tenant: str) -> bool:
        actor = _normalize_actor(actor)
        for user in self.users():
            if _normalize_actor(user["actor"]) == actor:
                tenants = user.get("tenants", ["*"])
                return "*" in tenants or tenant in tenants
        return False

    def _ensure_bootstrap(self) -> None:
        if self.path.exists():
            return
        bootstrap = [
            {
                "actor": "operator@example.local",
                "role": "admin",
                "tenants": ["*"],
                "enabled": True,
                "updated_at": datetime.now(UTC).isoformat(),
            },
            {
                "actor": "operator",
                "role": "admin",
                "tenants": ["*"],
                "enabled": True,
                "updated_at": datetime.now(UTC).isoformat(),
            },
        ]
        write_json(self.path, bootstrap)


def _normalize_actor(actor: str) -> str:
    return (actor or "anonymous").strip().lower()
