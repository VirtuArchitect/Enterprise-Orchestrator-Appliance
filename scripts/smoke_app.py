from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import urllib.request
from http.server import ThreadingHTTPServer

from enterprise_orchestrator.app import EnterpriseOrchestratorHandler


def main() -> None:
    with tempfile.TemporaryDirectory() as state_dir:
        os.environ["EOA_STATE_DIR"] = state_dir
        server = ThreadingHTTPServer(("127.0.0.1", 0), EnterpriseOrchestratorHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            health = get(port, "/api/health")
            assert health["status"] == "healthy", health

            evidence = post(
                port,
                "/api/evidence",
                {
                    "tenant": "smoke",
                    "submitted_by": "operator@example.local",
                    "source": "smoke-log",
                    "summary": "Synthetic smoke evidence",
                    "content": "No live infrastructure touched.",
                },
            )["evidence"]
            assert evidence["content_sha256"], evidence
            assert evidence["signature"], evidence

            evidence_verification = get(port, "/api/evidence/verify?tenant=smoke")
            assert evidence_verification["valid"] is True, evidence_verification

            request = post(
                port,
                "/api/requests",
                {
                    "tenant": "smoke",
                    "submitted_by": "operator@example.local",
                    "task": "Troubleshoot Nutanix storage latency with read-only checks.",
                    "requested_action_boundary": "T0",
                    "evidence_ids": [evidence["evidence_id"]],
                },
            )["request"]
            assert request["status"] == "ready_for_t0_execution", request

            execution = post(
                port,
                "/api/execute/dry-run",
                {"actor": "operator@example.local", "request": request},
            )["execution"]
            assert execution["status"] == "completed", execution

            audit = get(port, "/api/audit?tenant=smoke")
            assert audit["chain_valid"] is True, audit
            assert len(audit["events"]) >= 3, audit

            model_health = get(port, "/api/model/health")
            assert model_health["provider"] == "ollama", model_health

            connector_plan = post(
                port,
                "/api/connectors/read-only-plan",
                {
                    "tenant": "smoke",
                    "requested_by": "operator@example.local",
                    "domains": ["nutanix", "storage"],
                },
            )
            assert connector_plan["commands"], connector_plan

            semantic_search = get(
                port,
                "/api/evidence/semantic-search?tenant=smoke&q=live%20infrastructure",
            )
            assert semantic_search["evidence"], semantic_search

            eaap_status = get(port, "/api/integrations/eaap")
            assert eaap_status["configured"] is False, eaap_status

            backup = post(
                port,
                "/api/backup",
                {"tenant": "smoke", "requested_by": "operator@example.local"},
            )
            assert backup["backup"]["path"].endswith(".tar.gz"), backup

            update = post(
                port,
                "/api/updates/stage",
                {
                    "tenant": "smoke",
                    "requested_by": "operator@example.local",
                    "artifact_path": "internal/release.tar.gz",
                    "sha256": "abc123",
                    "version": "0.2.0",
                },
            )
            assert update["update"]["apply_enabled"] is False, update
            print("Application smoke test passed.")
        finally:
            server.shutdown()
            thread.join(timeout=5)
            time.sleep(0.1)


def get(port: int, path: str) -> dict[str, object]:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def post(port: int, path: str, payload: dict[str, object]) -> dict[str, object]:
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    main()
