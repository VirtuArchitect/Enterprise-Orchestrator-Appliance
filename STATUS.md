# Enterprise Orchestrator Appliance Status

This file records the current maturity boundary for the Enterprise Orchestrator
Appliance. Keep public claims aligned with implementation evidence.

## Summary

Area | Status | Evidence / boundary
--- | --- | ---
Repository foundation | Initialized | Project-specific README, status file, architecture docs, prompts, service boundaries, and validation script
Prompt policy pack | Scaffolded | `prompts/enterprise-orchestrator-v5.6.md` and output-contract schema placeholders exist
Custom operator UI | Planned | `ui/` boundary exists; no implementation yet
Local LLM adapter | Planned | `services/llm-adapter/` boundary exists; no runtime integration yet
Governed orchestrator API | Planned | `services/orchestrator-api/` boundary exists; no API implementation yet
Evidence service | Planned | `services/evidence-service/` boundary exists; no RAG or ingestion implementation yet
Approval, execution, audit integration | Planned | Service boundaries exist; no live EAAP integration yet
Docker Compose appliance profile | Planned | Deployment boundary exists; no runnable stack yet
AHV/RHEL deployable appliance | Not established | No QCOW2, installer, or air-gapped package has been produced
Production validation | Not established | No empirical enterprise deployment validation

## Validated Now

- Local repository has been initialized on `main`.
- The appliance architecture boundary is documented.
- The prompt/output-contract boundary is scaffolded.
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

- Implement contract validation for model output.
- Add a minimal orchestrator API with unit tests.
- Add an LLM adapter that can target Ollama first, then llama.cpp.
- Add Docker Compose for local development.
- Add UI screenshots and accessibility checks once the operator UI exists.
- Add an appliance update, backup, and health design before host-level mutation.
