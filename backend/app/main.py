"""Application entrypoint and FastAPI factory.

Configures database table initialization, optional startup demo data seeding,
CORS middleware, exception handlers, REST and WebSocket routers, and static media hosting.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app import models  # noqa: F401  (registers the tables on Base.metadata)
from app.api.routes import auth, contacts, conversations, health, messages, users
from app.core.config import get_settings
from app.core.errors import AppError, app_error_handler, validation_error_handler
from app.db import Base, SessionLocal, engine
from app.realtime import ws
from app.seed import seed


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """FastAPI lifespan context manager.

    Ensures database schemas exist before handling requests, and optionally seeds
    the demo accounts and conversations if the database is currently empty.
    """
    Base.metadata.create_all(engine)
    if get_settings().seed_on_startup:
        with SessionLocal() as db:
            if db.scalar(select(models.User.id).limit(1)) is None:
                seed(db)
    yield


def create_app() -> FastAPI:
    """Builds and configures the FastAPI application instance."""
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    # Allow cross-origin requests from configured frontends (e.g. Next.js dev server).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Register structured JSON error response handlers for business errors and validation failures.
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    # Health check is unversioned; core REST routes are nested under /api/v1.
    app.include_router(health.router)
    for module in (auth, users, contacts, conversations, messages):
        app.include_router(module.router, prefix="/api/v1")
    # WebSocket route mounted at the root /ws.
    app.include_router(ws.router)

    # Serve user avatars and media uploads as static files.
    media_dir = Path(settings.media_dir)
    media_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/media", StaticFiles(directory=media_dir), name="media")
    return app


# Singleton ASGI application instance.
app = create_app()

