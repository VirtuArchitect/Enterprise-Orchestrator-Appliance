# Appliance Image Build Evidence Template

Use this template when turning the plan-only AHV/RHEL workflow into a controlled
image build record.

## Build Inputs

- Source commit:
- Source artifact SHA256:
- Artifact manifest SHA256:
- SBOM SHA256:
- RHEL image or installation media:
- Offline Python/runtime bundle:
- Optional model runtime bundle:

## Build Environment

- Builder host:
- Network isolation:
- Output directory:
- Operator:
- Approver:

## Validation Evidence

- `scripts/validate_release_artifacts.py` output:
- `scripts/build_appliance_image.py` plan output:
- First boot evidence:
- `scripts/smoke_app.py` output:
- Vulnerability scan evidence:

## Boundary

This repository provides the governed build plan and validation hooks. It does
not claim that a QCOW2, AHV image, or production appliance image has been built
until this evidence is completed and reviewed.
