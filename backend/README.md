# Tripbox Backend

FastAPI server for Tripbox.

## Local development

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check it's running:

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

## Tests

```bash
.venv/bin/pytest
```
