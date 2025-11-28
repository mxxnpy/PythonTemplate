"""
FastAPI Application - configuracao da aplicacao
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.controllers import health_router, example_router
from src.infrastructure.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """lifecycle da aplicacao"""
    # startup
    yield
    # shutdown


def create_app() -> FastAPI:
    """cria e configura a aplicacao FastAPI"""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # controllers
    app.include_router(health_router)
    app.include_router(example_router)

    return app


# instancia global
app = create_app()
