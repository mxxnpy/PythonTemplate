"""
Example Repository - implementacao em memoria (para desenvolvimento/testes)
"""

from __future__ import annotations

from uuid import UUID

from src.core import Either, ErrorResult, Right
from src.core.option import Nothing, Option, Some
from src.domain.entities.example import Example
from src.domain.enums import Status


class InMemoryExampleRepository:
    """repositorio em memoria"""

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: dict[UUID, Example] = {}

    async def get_by_id(self, id: UUID) -> Option[Example]:
        """busca por id"""
        entity = self._data.get(id)
        if entity and entity.status != Status.DELETED:
            return Some(entity)
        return Nothing()

    async def get_by_name(self, name: str) -> Option[Example]:
        """busca por nome"""
        for entity in self._data.values():
            if entity.name == name and entity.status != Status.DELETED:
                return Some(entity)
        return Nothing()

    async def save(self, entity: Example) -> Either[ErrorResult, Example]:
        """salva entidade"""
        self._data[entity.id] = entity
        return Right(entity)

    async def delete(self, id: UUID) -> Either[ErrorResult, None]:
        """deleta entidade (soft delete)"""
        entity = self._data.get(id)
        if entity:
            entity.status = Status.DELETED
        return Right(None)

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[Example], int]:
        """lista paginado"""
        # filtra deletados
        items = [e for e in self._data.values() if e.status != Status.DELETED]
        total = len(items)

        # pagina
        start = (page - 1) * page_size
        end = start + page_size

        return items[start:end], total

    def clear(self) -> None:
        """limpa dados (para testes)"""
        self._data.clear()
