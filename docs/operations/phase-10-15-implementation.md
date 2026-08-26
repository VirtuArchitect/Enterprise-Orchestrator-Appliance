# Phase 10-15 Implementation Boundary

This increment advances the appliance from a local MVP baseline toward a
release-candidate control surface without claiming production validation.

## Implemented

- Phase 10: optional FastAPI runtime entrypoint through `enterprise_orchestrator.fastapi_app`.
- Phase 11: local role-based authorization for operator, approver, and admin flows.
- Phase 12: signed evidence records, evidence verification, and local semantic search.
- Phase 13: fail-closed EAAP control-plane handoff client and status endpoint.
- Phase 14: AHV/RHEL image build plan generator.
- Phase 15: release-gate script covering metadata generation, validation, tests,
  smoke checks, public hygiene scan, and diff hygiene.
- Demo control: `DEMO_URL`, `DEMO_STATUS`, and `docs/demo/index.html` keep the
  static demo reference aligned with release documentation.
  Reserved URL: https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/

## Not Claimed

- FastAPI is optional and not required by the default stdlib appliance server.
- The EAAP integration does not execute infrastructure work.
- The image build plan is not a produced or validated QCOW2 artifact.
- Release gates are project hygiene controls, not penetration testing,
  certification, or production assurance.
- The hosted demo is static only and does not connect to live infrastructure.
