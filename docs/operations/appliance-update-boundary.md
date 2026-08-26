# Appliance Update Boundary

Host-level appliance updates are not implemented yet.

Before adding update apply capability, the design must include:

- staged update request file
- artifact checksum validation
- pre-update backup of prompts, configuration, evidence, approvals, audit, and
  runtime state
- duplicate-run protection
- explicit administrator approval
- bounded systemd or equivalent runner
- post-update health checks
- rollback and recovery documentation

The operator UI may show update readiness in the future, but it must not perform
host mutation until the above controls are implemented and tested.
