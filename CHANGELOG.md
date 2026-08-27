# Changelog

## 0.3.0 - 2026-08-27

- Replaced the prompt scaffold with the governed Enterprise Multi-Agent
  Orchestrator v5.6 policy pack.
- Added console controls for semantic evidence search, evidence signature
  verification, prompt policy status, release status, and EAAP handoff status.
- Added left sidebar navigation for console, evidence, approvals, operations,
  history, audit, settings, and about sections.
- Added an OpenWebUI-compatible console roadmap with governed/deferred feature
  boundaries.
- Added optional FastAPI runtime validation and mock EAAP handoff validation to
  release gates.
- Added AHV/RHEL image-build execution checklist.
- Updated the static demo to present a richer appliance workflow snapshot.

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
- Added static demo artifact, reserved hosted URL, and demo-link validation:
  https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/
- Recorded demo publication state as `live` after GitHub Pages deployment
  succeeded.
- Added a public publication checklist.
- Added manual CI dispatch support for public-readiness verification.

## 0.1.0 - 2026-08-26

- Added dependency-free Enterprise Orchestrator local MVP.
- Added contract-first plan validation and governed envelopes.
- Added Ollama-compatible local LLM adapter with deterministic fallback.
- Added static operator UI.
- Added local evidence, approval, audit, dry-run execution, and appliance status
  services.
- Added Docker local appliance profile and AHV/RHEL packaging groundwork.
