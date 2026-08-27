# Operator UI

Dependency-free operator console served by `enterprise_orchestrator.app`.

The console opens in light mode by default. Operators can switch to dark mode
from the header, and the preference is stored locally in the browser.

Implemented user flow:

1. Submit infrastructure request.
2. Attach or paste evidence.
3. Review known and missing data.
4. Review domains, confidence, risk tier, validation, and rollback.
5. Route approval-required work to the governed approval path.
6. Inspect audit trail.
7. Inspect prompt policy, release status, evidence signatures, semantic search,
   and EAAP handoff status.
8. Navigate operator and admin sections from the left sidebar.

Run locally with:

```powershell
$env:PYTHONPATH = "src"
python -m enterprise_orchestrator.app
```
