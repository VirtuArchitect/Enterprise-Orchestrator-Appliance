# Services

Backend service boundaries for the appliance.

Service | Purpose
--- | ---
`orchestrator-api` | Request intake, classification, model-plan validation, governance handoff
`llm-adapter` | Local model runtime abstraction
`evidence-service` | Local evidence ingestion, retrieval, and provenance
`audit-service` | Immutable event recording and verification
`appliance-api` | Health, backup, restore, updates, configuration, and support bundles

These directories are placeholders until the runtime stack is selected.
