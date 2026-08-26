# Public Publication Checklist

This repository may be made public after the release gates pass and the project
claims remain aligned with `STATUS.md`.

## Required Before Public Visibility

- Run `PYTHONPATH=src python scripts/run_release_gates.py`.
- Confirm the public hygiene scan passes without sensitive-looking content.
- Confirm `DEMO_URL`, `DEMO_STATUS`, README, changelog, release notes, and the
  static demo page are aligned.
- Confirm the repository About description and topics are set for the appliance
  repository, not the EAAP control-plane reference implementation.
- Confirm the demo page is static and does not call live infrastructure APIs.

## Publication Boundary

Public visibility does not change the product maturity claim. The repository is
an EAAP-aligned local appliance foundation and maturity increment, not a
production-ready autonomous infrastructure operator, certification, or
validated AHV/RHEL image.

## Demo URL

Reserved URL: https://virtuarchitect.github.io/Enterprise-Orchestrator-Appliance/

`DEMO_STATUS` is the source of truth for whether that reserved URL is live.
