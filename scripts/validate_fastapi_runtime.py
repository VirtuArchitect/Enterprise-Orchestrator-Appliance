from __future__ import annotations

import json


def main() -> None:
    try:
        from enterprise_orchestrator.fastapi_app import create_app
        app = create_app()
    except RuntimeError as exc:
        print(f"FastAPI runtime validation skipped: {exc}")
        return

    routes = sorted(route.path for route in app.routes)
    required = {
        "/api/health",
        "/api/evidence",
        "/api/evidence/verify",
        "/api/evidence/semantic-search",
        "/api/integrations/eaap",
        "/api/prompt-policy",
        "/api/release/status",
    }
    missing = sorted(required - set(routes))
    if missing:
        raise SystemExit("FastAPI runtime missing routes: " + ", ".join(missing))
    print(json.dumps({"fastapi_runtime": "available", "routes": routes}, indent=2))


if __name__ == "__main__":
    main()
