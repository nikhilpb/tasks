from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Family Task Manager API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(f"{settings.api_prefix}/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.app_env}

    @app.get(f"{settings.api_prefix}")
    def api_root() -> dict[str, str]:
        return {"name": "family-task-backend", "status": "ok"}

    return app


app = create_app()
