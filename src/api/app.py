"""
FastAPI Application - configuracao da aplicacao
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.controllers import example_router, health_router
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
        description="API Template seguindo AYU CODE STYLE",
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
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
