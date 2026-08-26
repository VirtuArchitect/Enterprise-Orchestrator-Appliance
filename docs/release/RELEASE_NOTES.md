# Release Notes

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
