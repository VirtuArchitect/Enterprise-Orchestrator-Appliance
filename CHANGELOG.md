# Changelog

## 0.2.0 - 2026-08-26

- Added optional FastAPI runtime entrypoint without removing the stdlib
  appliance server.
- Added local RBAC and tenant-scoped authorization gates.
- Added signed evidence records, evidence verification, and dependency-free
  semantic evidence search.
- Added fail-closed EAAP control-plane handoff client and status endpoint.
- Added AHV/RHEL appliance image-build planning artifact.
- Added Phase 15 release gates for metadata generation, tests, smoke checks,
  public hygiene scanning, Docker Compose validation, and diff hygiene.
- Added static demo publication workflow and demo-link validation:
  https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/

## 0.1.0 - 2026-08-26

- Added dependency-free Enterprise Orchestrator local MVP.
- Added contract-first plan validation and governed envelopes.
- Added Ollama-compatible local LLM adapter with deterministic fallback.
- Added static operator UI.
- Added local evidence, approval, audit, dry-run execution, and appliance status
  services.
- Added Docker local appliance profile and AHV/RHEL packaging groundwork.
