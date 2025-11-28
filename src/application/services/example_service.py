"""
Example Service - logica de negocio para Example
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.core import Either, ErrorResult, Left, Right
from src.core.option import Nothing, Option, Some, to_either
from src.application.specifications.example_specs import (
    NameNotEmptySpec,
    ValuePositiveSpec,
)
from src.domain.entities.example import Example


# protocol do repositorio
class ExampleRepository(Protocol):
    """interface do repositorio"""

    async def get_by_id(self, id: UUID) -> Option[Example]: ...
    async def get_by_name(self, name: str) -> Option[Example]: ...
    async def save(self, entity: Example) -> Either[ErrorResult, Example]: ...
    async def delete(self, id: UUID) -> Either[ErrorResult, None]: ...
    async def list_all(self, page: int, page_size: int) -> tuple[list[Example], int]: ...


class ExampleService:
    """service com logica de negocio"""

    __slots__ = ("_repo",)

    def __init__(self, repo: ExampleRepository):
        self._repo = repo

    async def create(
        self,
        name: str,
        description: str = "",
        value: int = 0,
    ) -> Either[ErrorResult, Example]:
        """cria novo exemplo"""

        # valida nome
        name_spec = NameNotEmptySpec()
        if not name_spec.is_satisfied_by(name):
            return Left(ErrorResult.validation(name_spec.error_message))

        # verifica duplicidade
        existing = await self._repo.get_by_name(name)
        if isinstance(existing, Some):
            return Left(ErrorResult.validation("Nome ja existe"))

        # cria e salva
        entity = Example.create(name=name, description=description, value=value)
        return await self._repo.save(entity)

    async def get_by_id(self, id: UUID) -> Either[ErrorResult, Example]:
        """busca por id"""
        result = await self._repo.get_by_id(id)
        return to_either(result, ErrorResult.not_found("Nao encontrado"))

    async def update(
        self,
        id: UUID,
        name: str | None = None,
        description: str | None = None,
        value: int | None = None,
    ) -> Either[ErrorResult, Example]:
        """atualiza exemplo"""

        # busca
        entity_result = await self.get_by_id(id)
        if isinstance(entity_result, Left):
            return entity_result

        entity = entity_result.value

        # atualiza campos
        if name is not None:
            name_spec = NameNotEmptySpec()
            if not name_spec.is_satisfied_by(name):
                return Left(ErrorResult.validation(name_spec.error_message))
            entity.name = name

        if description is not None:
            entity.description = description

        if value is not None:
            entity.value = value

        entity.mark_updated()
        return await self._repo.save(entity)

    async def delete(self, id: UUID) -> Either[ErrorResult, None]:
        """deleta exemplo"""
        return await self._repo.delete(id)

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[Example], int]:
        """lista paginado"""
        return await self._repo.list_all(page, page_size)

