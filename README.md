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
  -> Static or optional FastAPI-hosted operator UI/API
  -> EAAP orchestrator API
  -> LLM adapter
  -> Local model runtime
  -> Governance, evidence, approval, execution gateway, and audit services
```

The LLM produces plans and recommendations. Deterministic services enforce
governance, approval, execution boundaries, rollback requirements, and audit.

## Demo

Static demo artifact: `docs/demo/index.html`

Reserved hosted URL:
https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/

The demo artifact is a static snapshot of the operator console. It demonstrates
the governed workflow and maturity boundary without connecting to live services
or infrastructure. The hosted URL is stored in `DEMO_URL`, and the current
publication state is stored in `DEMO_STATUS`. Release gates validate both so
future updates keep the demo reference current.

Current publication state: `live`.

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

1. Install and validate the optional FastAPI runtime profile.
2. Connect the fail-closed EAAP handoff client to a real control-plane
   environment.
3. Build and validate an actual AHV/RHEL appliance image.
4. Replace local bootstrap RBAC with an enterprise identity provider.
5. Add external vector/RAG infrastructure once a storage and security model is
   approved.

The OpenWebUI-compatible console backlog is tracked in
`docs/roadmap/openwebui-compatible-console.md`.

The governed system prompt is tracked in
`prompts/enterprise-orchestrator-v5.6.md` and validated by
`scripts/validate_prompt_policy.py`.

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

Run the Phase 15 release gates with:

```powershell
$env:PYTHONPATH = "src"
python scripts/run_release_gates.py
```

Start the local operator console with:

```powershell
$env:PYTHONPATH = "src"
python -m enterprise_orchestrator.app
```
