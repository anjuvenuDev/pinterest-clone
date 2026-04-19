# Pinterest Clone (Expo + React Native + FastAPI)

A Pinterest-style mobile app built with Expo Router, React Native, and TypeScript, now integrated with a FastAPI backend gateway.

## Tech Stack

- Frontend: Expo SDK 54, Expo Router, React Native 0.81, React 19, TypeScript
- Backend: FastAPI, service-layer architecture, async worker queue stubs
- Data Layer: Supabase-style repository interface (in-memory local mode)

## Architecture (Implemented)

- React Native app -> FastAPI gateway
- Gateway concerns: auth middleware, rate limiting, routing
- Domain modules:
  - Recipe + Feed
  - User + Auth
  - Creator Ingestion
  - Remix Engine
- Data services:
  - Supabase/Postgres abstraction
  - background queues: search indexing, scraper jobs, feed ranking
  - external adapters: OpenAI/Claude, Supabase Storage, Typesense/Algolia, Expo Push (stubbed)

## Frontend API Integration

The screens now call backend endpoints with graceful fallback to local pins when backend is unreachable:

- `HomeScreen` -> `GET /api/feed`
- `PinScreen` -> `GET /api/feed/{recipe_id}`
- `CreatePinScreen` -> `POST /api/creator/ingest`
- `ProfileScreen` -> `GET /api/users/me` and `GET /api/feed?bookmarked=true`
- `Pin` component like action -> `POST /api/feed/{recipe_id}/like`

## Project Structure

- `app/(tabs)/HomeScreen.tsx` - home feed
- `app/PinScreen.tsx` - pin details
- `app/(tabs)/CreatePinScreen.tsx` - creator ingestion flow
- `app/(tabs)/ProfileScreen.tsx` - profile + bookmarks
- `services/api.ts` - typed frontend backend client
- `types/pin.ts` - shared frontend data contracts
- `backend/` - FastAPI backend services
- `BACKEND_INTEGRATION_STEPS.txt` - step-by-step integration log

## Environment Variables

Create `.env` for Expo app:

```bash
EXPO_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
EXPO_PUBLIC_DEMO_TOKEN=demo-token
```

Notes:
- Android emulator usually requires `http://10.0.2.2:8000/api`.
- iOS simulator/web can use `http://127.0.0.1:8000/api`.
- Physical device should use your laptop LAN IP, e.g. `http://192.168.1.10:8000/api`.
- If `EXPO_PUBLIC_API_BASE_URL` is omitted, app will try to infer Expo host LAN IP automatically.

## Run Frontend

```bash
npm install
npx expo start
```

## Run Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

For mobile devices on the same Wi-Fi network, keep `--host 0.0.0.0` and ensure your firewall allows incoming traffic on port `8000`.

If port 8000 is occupied, use another port and update frontend env:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Then set `EXPO_PUBLIC_API_BASE_URL=http://<host>:8001/api`.

## Test Backend

```bash
cd /home/anj/Pinterest
source backend/.venv/bin/activate
PYTHONPATH=backend pytest -q backend/tests
```

## Type Check Frontend

```bash
npx tsc --noEmit
```

## Development Log

Detailed integration checkpoints are documented in:

- `BACKEND_INTEGRATION_STEPS.txt`
