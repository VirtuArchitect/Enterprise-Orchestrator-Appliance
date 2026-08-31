# EAAP Integration Validation

The Enterprise Orchestrator Appliance can be configured to hand governed plans
to an EAAP control plane by setting `EOA_EAAP_CONTROL_PLANE_URL`.

The integration remains plan-handoff only:

- the local LLM proposes a governed plan;
- local governance evaluates the output contract;
- approvals and evidence remain appliance-visible;
- the EAAP client posts to `/api/plan-handoffs` only when configured;
- no local infrastructure mutation is enabled by this integration.

Run:

```text
PYTHONPATH=src python scripts/validate_eaap_integration_config.py
```

When the URL is unset, validation reports a skipped state. That is the expected
offline default for an appliance build or public demo.
