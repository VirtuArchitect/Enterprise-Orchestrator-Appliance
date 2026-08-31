# Enterprise Identity Adapter Path

The appliance currently uses a local bootstrap identity store for controlled
operator workflows. Enterprise identity is exposed as an adapter status path so
OIDC or SAML integration can be added without weakening the current fail-closed
RBAC boundary.

## Modes

- `local-bootstrap`: default local JSON-backed users and roles.
- `oidc-planned`: declared future integration path.
- `saml-planned`: declared future integration path.

`EOA_IDENTITY_MODE` selects the declared mode. `EOA_IDENTITY_ISSUER_URL` marks an
enterprise issuer as configured for planning purposes only. The current
reference appliance does not enforce OIDC or SAML tokens.

## Boundary

Local RBAC remains authoritative until a verified adapter is implemented,
tested, and documented. Unknown users fail closed to viewer permissions with no
tenant access.
