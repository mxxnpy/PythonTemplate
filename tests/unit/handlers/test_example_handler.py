"""
Tests for Example Handler
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from src.core import Left, Right
from src.application.handlers.example_handler import (
    CreateExampleCommand,
    ExampleHandler,
    GetByIdQuery,
    ListAllQuery,
)
from src.application.services.example_service import ExampleService
from src.infrastructure.repositories.example_repository import InMemoryExampleRepository


@pytest.fixture
def handler() -> ExampleHandler:
    """retorna handler configurado"""
    repo = InMemoryExampleRepository()
    service = ExampleService(repo)
    return ExampleHandler(service)


class TestCreateExample:
    """testes para criacao"""

    @pytest.mark.asyncio
    async def test_create_success(self, handler: ExampleHandler) -> None:
        cmd = CreateExampleCommand(name="Test", description="Desc", value=10)
        result = await handler.create(cmd)

        assert result.is_right
        assert result.value.name == "Test"

    @pytest.mark.asyncio
    async def test_create_empty_name_fails(self, handler: ExampleHandler) -> None:
        cmd = CreateExampleCommand(name="", value=10)
        result = await handler.create(cmd)

        assert isinstance(result, Left)


class TestGetById:
    """testes para busca por id"""

    @pytest.mark.asyncio
    async def test_get_existing_returns_entity(self, handler: ExampleHandler) -> None:
        # cria primeiro
        cmd = CreateExampleCommand(name="Test")
        created = await handler.create(cmd)
        entity_id = created.value.id

        # busca
        query = GetByIdQuery(id=entity_id)
        result = await handler.get_by_id(query)

        assert result.is_right
        assert result.value.id == entity_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_returns_not_found(self, handler: ExampleHandler) -> None:
        query = GetByIdQuery(id=uuid4())
        result = await handler.get_by_id(query)

        assert isinstance(result, Left)
        assert result.value.is_not_found


class TestListAll:
    """testes para listagem"""

    @pytest.mark.asyncio
    async def test_list_empty_returns_empty(self, handler: ExampleHandler) -> None:
        query = ListAllQuery()
        result = await handler.list_all(query)

        assert len(result.items) == 0
        assert result.total == 0

    @pytest.mark.asyncio
    async def test_list_with_data_returns_items(self, handler: ExampleHandler) -> None:
        # cria alguns
        for i in range(5):
            await handler.create(CreateExampleCommand(name=f"Item {i}"))

        query = ListAllQuery()
        result = await handler.list_all(query)

        assert len(result.items) == 5
        assert result.total == 5

    @pytest.mark.asyncio
    async def test_list_pagination_works(self, handler: ExampleHandler) -> None:
        # cria 15 itens
        for i in range(15):
            await handler.create(CreateExampleCommand(name=f"Item {i}"))

        query = ListAllQuery(page=1, page_size=5)
        result = await handler.list_all(query)

        assert len(result.items) == 5
        assert result.total == 15
        assert result.page == 1
        assert result.total_pages == 3

