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

This repository is at foundation stage. See `STATUS.md` for the current maturity
boundary and claims to avoid.

## First Milestones

1. Define the prompt output contract and validation schema.
2. Build a minimal orchestrator API that accepts a request and returns a
   governed planning envelope.
3. Add a local LLM adapter for Ollama or llama.cpp.
4. Build the first operator UI flow: request intake, missing evidence, risk tier,
   confidence, approval state, validation, and rollback.
5. Add Docker Compose for local appliance development.

## Verification

The repository currently provides a scaffold validation command:

```powershell
python scripts/validate_repository.py
```

This check verifies that the first architecture, prompt, service, deployment,
and governance files exist.
