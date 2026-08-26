# Architecture Overview

Enterprise Orchestrator Appliance is an EAAP-aligned local operations appliance.
It embeds a local LLM runtime behind deterministic governance and audit
boundaries.

## Core Boundary

The model may reason, classify, summarize, and propose. It must not directly
execute infrastructure actions. All execution-capable work must pass through
governed APIs that enforce evidence, risk tier, approval, rollback, and audit.

## Logical Components

Component | Responsibility | Current state
--- | ---
Operator UI | Guided request intake, evidence capture, plan review, approval state, audit visibility | Static MVP
Orchestrator API | Request classification, domain routing, output-contract validation, governance handoff | Stdlib HTTP MVP
LLM Adapter | Local model runtime abstraction for Ollama, llama.cpp, or future offline runtimes | Ollama plus deterministic fallback
Evidence Service | Local document, log, and runbook ingestion with provenance tracking | JSON local store
Approval Workflow | Human approval for actions above configured risk thresholds | Local plan-hash-bound queue
Execution Gateway | Sole interface for infrastructure-mutating connectors | Dry-run only
Audit Service | Immutable event trail for requests, decisions, approvals, execution, and validation | JSONL hash chain
Appliance API | Health, runtime config, backup, restore, update, and support-bundle surfaces | Health/status only

## Default Request Flow

```text
Operator submits request
  -> Orchestrator records request
  -> Evidence service attaches available context
  -> LLM adapter produces structured planning draft
  -> Orchestrator validates output contract
  -> Governance evaluates evidence, confidence, risk, and approval requirements
  -> UI presents approval-ready plan or missing-evidence request
  -> Approved actions route only through execution gateway
  -> Audit records each state transition
```

## Air-Gapped Assumptions

- Runtime must work without internet access.
- Model artifacts, container images, packages, prompts, and schemas must be
  transferred through controlled internal artifact paths.
- Image tags and package versions must be pinned.
- Checksums should be generated and validated at every transfer boundary.
