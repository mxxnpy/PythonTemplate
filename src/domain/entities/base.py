"""
Entity Base - Classe base para entidades do dominio
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID, uuid4

Id = TypeVar("Id")


@dataclass
class Entity(Generic[Id]):
    """classe base para entidades"""

    id: Id


@dataclass
class AuditableEntity(Entity[Id]):
    """entidade com campos de auditoria"""

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    created_by: str | None = None
    updated_by: str | None = None

    def mark_updated(self, by: str | None = None) -> None:
        """marca entidade como atualizada"""
        self.updated_at = datetime.now(UTC)
        self.updated_by = by


@dataclass
class SoftDeletableEntity(AuditableEntity[Id]):
    """entidade com soft delete"""

    deleted_at: datetime | None = None
    deleted_by: str | None = None
    is_deleted: bool = False

    def soft_delete(self, by: str | None = None) -> None:
        """marca entidade como deletada"""
        self.deleted_at = datetime.now(UTC)
        self.deleted_by = by
        self.is_deleted = True

    def restore(self) -> None:
        """restaura entidade deletada"""
        self.deleted_at = None
        self.deleted_by = None
        self.is_deleted = False


# helpers
def generate_uuid() -> UUID:
    """gera um novo UUID"""
    return uuid4()
