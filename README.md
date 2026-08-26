# Enterprise Orchestrator Appliance

Air-gapped operator console and local LLM appliance aligned to the Enterprise AI
Architecture Pattern (EAAP) control-plane model.

## What This Is

Enterprise Orchestrator Appliance is intended to replace a generic OpenWebUI
front end with a purpose-built operations interface. The appliance embeds a
local model runtime behind governed EAAP services so infrastructure questions can
be converted into evidence-backed, risk-tiered, approval-ready plans.

It is:

- An operator-facing reasoning console for infrastructure triage and planning.
- A local LLM integration boundary for offline enterprise environments.
- A prompt and policy-pack host with versioned output contracts.
- An appliance-oriented deployment target for Docker and Nutanix AHV/RHEL use.

It is not:

- A production-ready autonomous infrastructure operator.
- A replacement for deterministic governance, approval, execution, or audit.
- A system where the LLM directly accesses or mutates infrastructure.

## Target Architecture

```text
Operator
  -> React operator UI
  -> EAAP orchestrator API
  -> LLM adapter
  -> Local model runtime
  -> Governance, evidence, approval, execution gateway, and audit services
```

The LLM produces plans and recommendations. Deterministic services enforce
governance, approval, execution boundaries, rollback requirements, and audit.

## Repository Layout

```text
docs/                         Architecture, security, operations, and testing
prompts/                      Versioned prompt and schema policy packs
services/                     Backend service boundaries
  appliance-api/              Health, config, backup, and update surface
  audit-service/              Immutable audit event service
  evidence-service/           Local evidence ingestion and retrieval
  llm-adapter/                Local model runtime gateway
  orchestrator-api/           Request intake and plan orchestration
ui/                           Future React operator console
deployments/                  Docker and appliance packaging assets
scripts/                      Local validation and project utilities
tests/                        Unit, integration, and smoke tests
```

## Current Status

This repository is at local MVP stage. See `STATUS.md` for the current maturity
boundary and claims to avoid. The current implementation is dependency-free
Python plus a static operator UI.

## First Milestones

1. Promote the stdlib API facade to FastAPI or equivalent when dependencies are
   explicitly approved.
2. Add signed evidence policy and vector retrieval.
3. Add live EAAP control-plane service integration.
4. Build and validate an actual AHV/RHEL appliance image.
5. Replace local-only identity placeholders with an enterprise identity model.

## Verification

The repository currently provides a scaffold validation command:

```powershell
python scripts/validate_repository.py
```

This check verifies that the first architecture, prompt, service, deployment,
and governance files exist.

Run the Phase 1 unit tests with:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

Run the local MVP smoke test with:

```powershell
$env:PYTHONPATH = "src"
python scripts/smoke_app.py
```

Start the local operator console with:

```powershell
$env:PYTHONPATH = "src"
python -m enterprise_orchestrator.app
```
