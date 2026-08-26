# Orchestrator API

Phase 1 implements the dependency-free orchestration core in
`src/enterprise_orchestrator/orchestrator_api/`.

Implemented:

- model output validation against `prompts/output-contract.schema.json`
- governed planning envelope generation
- low-confidence blocking
- approval routing for Tier 1 and above
- disruptive-action checks for rollback and validation metadata

Not implemented yet:

- HTTP API wrapper
- persistence
- live governance service integration
- local LLM adapter integration
