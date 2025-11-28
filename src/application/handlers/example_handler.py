"""
Example Handler - casos de uso para Example
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.application.services.example_service import ExampleService
from src.application.view_models import ExampleResponse, PaginatedResult
from src.core import Either, ErrorResult, map_right
from src.domain.entities.example import Example


# commands/queries
@dataclass(frozen=True, slots=True)
class CreateExampleCommand:
    """comando para criar"""

    name: str
    description: str = ""
    value: int = 0


@dataclass(frozen=True, slots=True)
class UpdateExampleCommand:
    """comando para atualizar"""

    id: UUID
    name: str | None = None
    description: str | None = None
    value: int | None = None


@dataclass(frozen=True, slots=True)
class GetByIdQuery:
    """query para buscar por id"""

    id: UUID


@dataclass(frozen=True, slots=True)
class ListAllQuery:
    """query para listar"""

    page: int = 1
    page_size: int = 10


# mapper
def to_response(entity: Example) -> ExampleResponse:
    """converte entidade para response"""
    return ExampleResponse(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        value=entity.value,
        status=entity.status.value,
    )


# handler
class ExampleHandler:
    """handler com casos de uso"""

    __slots__ = ("_service",)

    def __init__(self, service: ExampleService):
        self._service = service

    async def create(self, cmd: CreateExampleCommand) -> Either[ErrorResult, ExampleResponse]:
        """cria novo exemplo"""
        result = await self._service.create(
            name=cmd.name,
            description=cmd.description,
            value=cmd.value,
        )
        return map_right(result, to_response)

    async def get_by_id(self, query: GetByIdQuery) -> Either[ErrorResult, ExampleResponse]:
        """busca por id"""
        result = await self._service.get_by_id(query.id)
        return map_right(result, to_response)

    async def update(self, cmd: UpdateExampleCommand) -> Either[ErrorResult, ExampleResponse]:
        """atualiza exemplo"""
        result = await self._service.update(
            id=cmd.id,
            name=cmd.name,
            description=cmd.description,
            value=cmd.value,
        )
        return map_right(result, to_response)

    async def delete(self, id: UUID) -> Either[ErrorResult, None]:
        """deleta exemplo"""
        return await self._service.delete(id)

    async def list_all(self, query: ListAllQuery) -> PaginatedResult[ExampleResponse]:
        """lista paginado"""
        items, total = await self._service.list_all(query.page, query.page_size)
        return PaginatedResult.create(
            items=[to_response(e) for e in items],
            total=total,
            page=query.page,
            page_size=query.page_size,
        )
