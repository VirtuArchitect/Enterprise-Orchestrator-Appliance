# AHV/RHEL Image Build Checklist

This checklist turns the Phase 14 image-build plan into an executable operator
runbook. It is not evidence that an image has been produced.

## Inputs

- Approved RHEL base image or installation media.
- Offline source artifact with `artifact-manifest.json`.
- Offline Python runtime and optional API wheelhouse.
- Local model runtime bundle or approved Ollama model cache.
- Appliance service unit and first-boot script.

## Build Steps

1. Create the base RHEL VM on Nutanix AHV.
2. Create the `enterprise-orchestrator` service account.
3. Install the source artifact under `/opt/enterprise-orchestrator`.
4. Create `/var/lib/enterprise-orchestrator` with owner-only permissions.
5. Install `enterprise-orchestrator.service`.
6. Run `firstboot.sh` and verify it creates only local bootstrap state.
7. Start the service and call `/api/health`.
8. Run `PYTHONPATH=src python scripts/smoke_app.py`.
9. Shut down the VM and capture the image.
10. Boot a clone and repeat `/api/health` plus the smoke test.

## Evidence To Capture

- Image source and checksum.
- Source artifact checksum.
- Service status output.
- `/api/health` response.
- Smoke-test output.
- Demo URL and release version.
- Known residual risks.

## Claim Boundary

Do not claim deployable AHV/RHEL appliance status until a captured image has
booted successfully and the evidence above is attached to the release record.
