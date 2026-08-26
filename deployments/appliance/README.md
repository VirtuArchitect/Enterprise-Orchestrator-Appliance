# Appliance Packaging

AHV/RHEL appliance packaging boundary.

Do not add host-mutating update flows until the backup, checksum, staging,
approval, rollback, and post-update health model is documented and tested.

Current state:

- Docker local appliance profile exists.
- AHV/RHEL image build automation is not implemented.
- Host-level update apply is not implemented.
- `firstboot.sh` prepares local state and generates a bootstrap token when run
  by an appliance build or administrator.
- `scripts/generate_artifact_manifest.py` creates a source artifact checksum
  manifest.
- `scripts/create_support_bundle.py` exports non-secret support context.
