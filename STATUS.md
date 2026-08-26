# Enterprise Orchestrator Appliance Status

This file records the current maturity boundary for the Enterprise Orchestrator
Appliance. Keep public claims aligned with implementation evidence.

## Summary

Area | Status | Evidence / boundary
--- | --- | ---
Repository foundation | Initialized | Project-specific README, status file, architecture docs, prompts, service boundaries, and validation script
Prompt policy pack | Scaffolded | `prompts/enterprise-orchestrator-v5.6.md` exists; output contract is implemented as a Phase 1 schema
Contract validation core | Implemented, Phase 1 | Dependency-free Python validator covers required fields, enums, arrays, objects, and additional-property blocking
Governed orchestrator API | Implemented, local MVP | Stdlib HTTP facade supports health, evidence, requests, approvals, audit, and dry-run execution
Custom operator UI | Implemented, local MVP | Static dependency-free UI supports request intake, evidence, plan review, approvals, dry-run, and audit
Local LLM adapter | Implemented, local MVP | Ollama-compatible adapter exists; deterministic fallback keeps offline smoke tests stable
Evidence service | Implemented, local MVP | JSON local evidence store with tenant filtering exists; no RAG yet
Evidence retrieval | Implemented, local MVP | Keyword search exists; vector/RAG retrieval is not implemented
Approval workflow | Implemented, local MVP | Plan-hash-bound local approval queue exists
Execution gateway | Implemented, dry-run only | Non-dry-run modes fail closed; T1+ dry-runs require approval
Read-only connector framework | Implemented, local MVP | Connector catalogue returns approved diagnostic command plans only; it does not execute commands
Audit service | Implemented, local MVP | JSONL tamper-evident hash chain exists
Appliance operations | Implemented, local MVP | Backup creation, support-bundle export script, and update staging exist; update apply is disabled
Release candidate assets | Implemented, local MVP | Version, changelog, release notes, SBOM generation, and artifact manifest exist
MVP baseline control | Implemented, Phase 9 | Release metadata, tests, smoke checks, and local status evidence are refreshed before baseline commit/tag
Docker Compose appliance profile | Implemented, local validation | Docker profile exists with digest-pinned Python base; Ollama overlay image still needs release pinning before offline release
AHV/RHEL deployable appliance | Scaffolded | First-boot script, systemd unit, and AHV/RHEL runbook exist; no QCOW2, installer, or air-gapped image has been produced
Production validation | Not established | No empirical enterprise deployment validation

## Validated Now

- Local repository has been initialized on `main`.
- The appliance architecture boundary is documented.
- The prompt/output-contract boundary is scaffolded and schema-validated.
- Phase 1 unit tests cover valid, invalid, low-confidence, approval-required,
  and disruptive-plan-without-rollback paths.
- Local MVP covers LLM adapter, operator UI, evidence, approval, dry-run gateway,
  audit chain, and appliance status.
- Maturity increment covers API endpoint expansion, model health, keyword
  evidence retrieval, backup creation, update staging, read-only connector
  planning, release notes, SBOM generation, and AHV/RHEL service scaffolding.
- Phase 9 baseline preparation records the local MVP as a commit/tag candidate
  after repository validation, unit tests, smoke tests, and diff hygiene checks.
- A repository scaffold validation script exists.

## Claims To Avoid

Do not describe this repository as:

- production-ready
- production-grade
- certified
- formally proven
- peer reviewed
- an industry standard
- an autonomous infrastructure operator

Preferred wording:

- appliance foundation
- EAAP-aligned operator console
- air-gapped local LLM appliance concept
- production-oriented reference implementation once runtime evidence exists

## Next Alignment Work

- Promote the local API facade to FastAPI or equivalent once runtime
  dependencies are explicitly approved.
- Add signed evidence policy and vector retrieval.
- Add UI screenshots and accessibility checks.
- Build and validate an actual AHV/RHEL image before claiming deployable
  appliance status.
