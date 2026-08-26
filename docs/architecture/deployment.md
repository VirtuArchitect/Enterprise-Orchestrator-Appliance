# Deployment Model

The first supported deployment target is a local Docker Compose appliance profile
running on a controlled Linux host. Nutanix AHV/RHEL appliance packaging is a
later milestone after the local stack is validated.

## Target Profiles

Profile | Status | Purpose
--- | --- | ---
Local development | Planned | Developer workstation validation
Docker appliance | Planned | Single-host air-gapped deployment
AHV/RHEL appliance | Not established | Deployable enterprise appliance image

## Appliance Principles

- Services run from pinned container images or pinned host packages.
- Secrets are generated or injected at first boot; they are not committed to the
  repository.
- Backups must cover prompts, configuration, evidence indexes, approvals, audit
  records, and local state.
- Updates must stage artifacts first, validate checksums, create backups, apply
  in a bounded sequence, and run post-update health checks.

## Initial Runtime Choice

Ollama is the pragmatic first local-model target because it is simple to operate
and good enough for early appliance validation. llama.cpp should remain the lean
offline fallback. vLLM is a future throughput-oriented option.
