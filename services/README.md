# Services

Backend service boundaries for the appliance.

Service | Purpose | Current state
--- | ---
`orchestrator-api` | Request intake, classification, model-plan validation, governance handoff | Local MVP
`llm-adapter` | Local model runtime abstraction | Ollama adapter plus deterministic fallback
`evidence-service` | Local evidence ingestion, retrieval, and provenance | JSON store
`audit-service` | Immutable event recording and verification | JSONL hash chain
`appliance-api` | Health, backup, restore, updates, configuration, and support bundles | Health/status only

These directories preserve the service boundaries even while the first
implementation is dependency-free.
