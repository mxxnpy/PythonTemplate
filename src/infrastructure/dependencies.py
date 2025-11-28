"""
Dependencies - injecao de dependencias
"""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.application.handlers.example_handler import ExampleHandler
from src.application.services.example_service import ExampleService
from src.infrastructure.config import Settings, get_settings
from src.infrastructure.repositories.example_repository import InMemoryExampleRepository


# repositorios (singleton)
@lru_cache
def get_example_repository() -> InMemoryExampleRepository:
    """retorna repositorio"""
    return InMemoryExampleRepository()


# services
def get_example_service(
    repo: Annotated[InMemoryExampleRepository, Depends(get_example_repository)],
) -> ExampleService:
    """retorna service"""
    return ExampleService(repo)


# handlers
def get_example_handler(
    service: Annotated[ExampleService, Depends(get_example_service)],
) -> ExampleHandler:
    """retorna handler"""
    return ExampleHandler(service)


# type aliases para DI
ExampleRepoDep = Annotated[InMemoryExampleRepository, Depends(get_example_repository)]
ExampleServiceDep = Annotated[ExampleService, Depends(get_example_service)]
ExampleHandlerDep = Annotated[ExampleHandler, Depends(get_example_handler)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
