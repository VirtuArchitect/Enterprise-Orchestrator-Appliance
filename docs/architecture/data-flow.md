# Data Flow

## Request Data

Operator requests enter through the UI and are submitted to the orchestrator API.
The request should include:

- operator identity
- tenant or environment scope
- free-text task
- selected domains, when known
- pasted evidence, uploaded evidence, or references to internal evidence
- requested action boundary, when known

## Model Data

The LLM receives only the minimum context required for planning. The prompt pack
and output contract shape its response. Model output is treated as untrusted
until validated by deterministic services.

## Evidence Data

Evidence must carry provenance. Expected future evidence classes include:

- operator-provided logs
- command output
- internal runbooks
- architecture documents
- configuration exports
- prior audited plans

## Audit Data

Audit records should capture:

- request received
- evidence attached
- model plan generated
- contract validation result
- governance decision
- approval decision
- execution token issuance
- gateway execution result
- rollback and validation evidence
