#!/usr/bin/env sh
set -eu

STATE_DIR="${EOA_STATE_DIR:-/var/lib/enterprise-orchestrator}"
SECRETS_FILE="${STATE_DIR}/secrets.env"

mkdir -p "${STATE_DIR}"
chmod 700 "${STATE_DIR}"

if [ ! -f "${SECRETS_FILE}" ]; then
  umask 077
  {
    printf 'EOA_BOOTSTRAP_TOKEN='
    python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
  } > "${SECRETS_FILE}"
fi

printf 'Enterprise Orchestrator first boot prepared state at %s\n' "${STATE_DIR}"
