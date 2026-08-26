# Enterprise Orchestrator Prompt Pack v5.6

Status: scaffolded.

This file will hold the production-reviewed Enterprise Orchestrator system prompt
used by the local model runtime. Keep prompt changes versioned, reviewed, and
validated against the output contract.

## Required Boundaries

- The model is a reasoning component, not the control plane.
- The model must classify known, missing, and required data before conclusions.
- Low-confidence responses must ask for validation data rather than assert root
  cause.
- Tier 2 and Tier 3 actions require explicit approval and rollback metadata.
- The model must not request secrets or invent versions, CVEs, commands, or
  evidence.

## Output Contract

Model responses must satisfy `prompts/output-contract.schema.json` before they
can become governed plans.
