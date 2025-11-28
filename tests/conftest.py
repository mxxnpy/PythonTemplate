"""
Conftest - fixtures compartilhadas
"""

from __future__ import annotations

import pytest

from src.domain.entities.example import Example
from src.domain.enums import Status
from src.infrastructure.repositories.example_repository import InMemoryExampleRepository


@pytest.fixture
def repository() -> InMemoryExampleRepository:
    """retorna repositorio limpo"""
    return InMemoryExampleRepository()


@pytest.fixture
def sample_entity() -> Example:
    """retorna entidade de exemplo"""
    return Example.create(name="Test", description="Test description", value=100)


@pytest.fixture
def active_entity() -> Example:
    """retorna entidade ativa"""
    entity = Example.create(name="Active", value=50)
    entity.activate()
    return entity
