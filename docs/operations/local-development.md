# Local Development

Run the dependency-free appliance MVP locally:

```powershell
$env:PYTHONPATH = "src"
$env:EOA_STATE_DIR = ".local-state"
python -m enterprise_orchestrator.app
```

Open `http://127.0.0.1:8085`.

Run the smoke test:

```powershell
$env:PYTHONPATH = "src"
python scripts/smoke_app.py
```

The smoke test uses temporary local state and does not contact infrastructure.
