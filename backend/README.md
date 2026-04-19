# Backend (FastAPI Gateway)

This backend mirrors the architecture in the project diagram:

- FastAPI Gateway with auth middleware and rate limiting
- Domain modules: recipe feed, user/auth, creator ingestion
- Remix engine for ingredient swaps
- Supabase-style repository layer (currently in-memory storage mode)
- Async background worker queues: search indexing, scraper jobs, feed ranking
- External service adapters: OpenAI/Claude, Supabase Storage, Typesense/Algolia, Expo Push

## Run locally

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

```bash
cd backend
PYTHONPATH=. pytest -q
```
