# AI Document Q&A — RAG Backend

A production-style Retrieval-Augmented Generation (RAG) API. Users upload documents (PDF, DOCX, TXT), the system chunks and embeds them into a vector store, and answers questions grounded strictly in the uploaded content — with streaming responses, per-user isolation, and async background processing.

**Live API:** `https://your-app.onrender.com` (free tier — first request after inactivity may take 30-60s to cold start)
**Docs:** `https://your-app.onrender.com/docs`

## Features

- JWT authentication (signup/login), per-user document isolation
- Async document ingestion via Celery + Redis — uploads return instantly, processing happens in background
- Text extraction (PDF, DOCX, TXT) → chunking → embeddings (`sentence-transformers`, local, no external embedding API)
- Vector similarity search via PostgreSQL + `pgvector`
- RAG-grounded answers via Groq LLM API, with a streaming (token-by-token) endpoint
- Document status tracking (`processing` / `ready` / `failed`) with real error surfacing
- Rate limiting per user (`slowapi` + Redis)
- File storage on Supabase Storage (not local disk — safe for stateless/multi-instance deployment)
- Schema migrations via Alembic — no manual DB changes
- Health check endpoint verifying live DB + Redis connectivity
- Fully Dockerized (API + worker as separate containers/services)

## Tech Stack

| Layer | Tech |
|---|---|
| API | FastAPI |
| DB | PostgreSQL (Neon) + pgvector |
| Cache/Queue | Redis (Layerbase) |
| Background jobs | Celery |
| File storage | Supabase Storage |
| LLM | Groq (Llama 3.1) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Migrations | Alembic |
| Deployment | Docker, Render (Web Service + Background Worker) |

## Architecture

```
Client
  │
  ▼
FastAPI (auth, upload, ask, list, delete)
  │                              │
  ▼                              ▼
Supabase Storage          Celery Task Queue (Redis)
  (raw files)                    │
                                  ▼
                          Celery Worker
                    (extract → chunk → embed)
                                  │
                                  ▼
                        PostgreSQL + pgvector
                          (chunks, vectors)
                                  │
                                  ▼
                    Retrieval (on /ask-document)
                                  │
                                  ▼
                        Groq LLM (grounded answer)
```

## Local Setup

### Prerequisites
- Docker + Docker Compose
- Accounts: [Neon](https://neon.tech) (Postgres), [Layerbase](https://layerbase.com) (Redis), [Supabase](https://supabase.com) (Storage), [Groq](https://console.groq.com) (LLM API key)

### Steps

```bash
git clone <your-repo-url>
cd <repo-name>
cp .env.example .env
# fill in .env with your own Neon/Layerbase/Supabase/Groq credentials

# Enable pgvector on your Neon database (one-time)
psql "<your-neon-connection-string>" -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Apply migrations
pip install -r requirements.txt
alembic upgrade head

# Run everything
docker-compose up --build
```

API available at `http://localhost:8000`, docs at `http://localhost:8000/docs`.

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Create account, returns JWT |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/documents/upload` | Upload a document (PDF/DOCX/TXT, max 25MB) |
| GET | `/documents` | List current user's documents + status |
| DELETE | `/documents/{id}` | Delete a document and its chunks |
| POST | `/ask-document` | Ask a question, get a grounded answer + sources |
| POST | `/ask-document/stream` | Same, streamed token-by-token |
| GET | `/health` | Liveness + DB/Redis connectivity check |

All endpoints except `/auth/*` and `/health` require `Authorization: Bearer <token>`.

## Design Notes

- **Why Celery, not FastAPI `BackgroundTasks`**: ingestion survives process restarts and scales to multiple workers; in-process background tasks don't.
- **Why files aren't stored on local disk**: Render's free tier filesystem is ephemeral and not guaranteed shared between the API and worker processes — Supabase Storage keeps both stateless.
- **Why per-user rate limiting**: prevents one account from exhausting the shared Groq free-tier quota for all users.
- **Why Alembic instead of `create_all()`**: schema changes apply incrementally without dropping/losing existing data.

## Known Limitations

- Free-tier hosting (Render, Neon, Layerbase) sleeps after inactivity — first request may be slow.
- No automated test suite yet (planned).
- Embeddings run on CPU locally in the worker — fine for demo scale, would move to a hosted embedding API for high throughput.
