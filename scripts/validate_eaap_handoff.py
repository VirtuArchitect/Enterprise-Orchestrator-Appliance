from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from enterprise_orchestrator.eaap_integration import ControlPlaneClient


class MockControlPlaneHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/api/plan-handoffs":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        response = {
            "accepted": True,
            "mode": "plan_handoff_only",
            "received_request_id": payload["request"].get("request_id"),
        }
        data = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), MockControlPlaneHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        client = ControlPlaneClient(base_url=base_url)
        result = client.handoff_plan({"request_id": "req-validation"})
        if result["received_request_id"] != "req-validation":
            raise SystemExit(f"unexpected EAAP handoff response: {result}")
        print("EAAP handoff validation passed.")
    finally:
        server.shutdown()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
