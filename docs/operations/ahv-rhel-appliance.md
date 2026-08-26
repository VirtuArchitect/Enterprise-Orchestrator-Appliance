# AHV/RHEL Appliance Plan

This is the deployment boundary for a future Nutanix AHV/RHEL appliance.

## Target Shape

- RHEL-compatible base image.
- Non-root `eoa` runtime user.
- `/opt/enterprise-orchestrator` application path.
- `/var/lib/enterprise-orchestrator` persistent state path.
- `enterprise-orchestrator.service` systemd unit.
- First-boot secret generation through `deployments/appliance/firstboot.sh`.

## Validation Required Before Claiming A Deployable Appliance

- Build image from a pinned base artifact.
- Verify package and image checksums after every transfer.
- Boot on target AHV environment.
- Validate `/api/health`.
- Validate UI login or local access model once authentication exists.
- Validate backup and restore.
- Export support bundle.
- Confirm no default credentials or private keys exist in the image.

Current status: design and service-unit scaffold only. No AHV/RHEL image has
been built or validated.
