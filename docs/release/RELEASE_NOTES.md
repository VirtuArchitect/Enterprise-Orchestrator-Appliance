# Release Notes

## 0.2.0 Phase 10-15 Maturity Increment

This release candidate increment advances the appliance baseline with optional
API runtime, local authorization, stronger evidence handling, integration
handoff scaffolding, image-build planning, and release-gate automation.

Demo:

- https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/
- Status: `pending-pages-deployment`
- Static artifact: `docs/demo/index.html`

Validated:

- optional FastAPI entrypoint source contract
- local RBAC role and tenant checks
- signed evidence and tamper detection
- semantic evidence search
- fail-closed EAAP control-plane status and handoff boundary
- AHV/RHEL image-build plan generation
- Phase 15 release gates
- demo link validation
- Docker Compose base and Ollama overlay configuration

Boundaries:

- FastAPI dependencies are optional and not installed by default.
- EAAP integration is disabled unless explicitly configured.
- EAAP handoff remains plan-only and does not execute infrastructure changes.
- No QCOW2, installer, or air-gapped appliance image has been produced.
- Release gates are project controls, not a security certification.
- The reserved hosted demo URL is not live until GitHub Pages deploys
  successfully from the public repository.

## 0.1.0 Local MVP

This release candidate establishes the first Enterprise Orchestrator Appliance
local MVP.

Validated:

- contract validation
- governed planning envelopes
- deterministic local fallback planner
- operator UI smoke flow
- evidence store
- plan-hash-bound approvals
- tamper-evident audit chain
- dry-run-only execution gateway
- Docker local appliance image build
- container health endpoint

Boundaries:

- No live infrastructure execution.
- No host-level update apply.
- No production assurance claim.
- No AHV/RHEL image artifact yet.
- Ollama is supported as a configured adapter but was not required for the local
  deterministic smoke path.
