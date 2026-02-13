# Family Task Manager

Task 1 foundation scaffold for the Family Task Manager MVP.

## Prerequisites

- Python 3.12+
- Node.js 20+
- `uv`
- Docker + Docker Compose

## Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Backend API health endpoint: `http://localhost:8000/api/health`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend app: `http://localhost:5173`

## Full stack with Docker Compose

```bash
docker compose up --build
```

App through reverse proxy: `http://localhost:3000`

## Tests

```bash
cd backend && uv run pytest
cd frontend && npm run test -- --run
```
