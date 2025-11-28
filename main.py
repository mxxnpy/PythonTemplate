"""
Main - Ponto de entrada da aplicacao
"""

import uvicorn

from src.infrastructure.config import get_settings


def main() -> None:
    """inicia o servidor"""
    settings = get_settings()

    uvicorn.run(
        "src.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()

