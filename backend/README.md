# Backend

## Run locally

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

## Test

```bash
uv run pytest
```
