# Docker Deployment

This folder contains the first local appliance Docker profile.

Run the dependency-free profile:

```bash
docker compose -f deployments/docker/compose.yaml up --build
```

Run with an Ollama sidecar:

```bash
docker compose \
  -f deployments/docker/compose.yaml \
  -f deployments/docker/compose.ollama.yaml \
  up --build
```

Boundary: this is a local validation profile. Before release packaging, base
image digests and transferred artifacts must be pinned and checksum-verified.
