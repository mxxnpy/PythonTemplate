"""
Health Controller - endpoints de health check
"""

from fastapi import APIRouter

from src.infrastructure.config import get_settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health() -> dict[str, str]:
    """verifica se a api esta funcionando"""
    settings = get_settings()
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@router.get("/ready")
async def ready() -> dict[str, str]:
    """verifica se a api esta pronta"""
    return {"status": "ready"}

