"""
Example Entity - entidade de exemplo para guiar implementacoes
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from src.domain.entities.base import AuditableEntity, generate_uuid
from src.domain.enums import Status


@dataclass
class Example(AuditableEntity[UUID]):
    """entidade de exemplo"""

    id: UUID = field(default_factory=generate_uuid)
    name: str = ""
    description: str = ""
    value: int = 0
    status: Status = Status.PENDING

    @classmethod
    def create(cls, name: str, description: str = "", value: int = 0) -> Example:
        """cria nova entidade"""
        return cls(name=name, description=description, value=value)

    def activate(self) -> None:
        """ativa entidade"""
        self.status = Status.ACTIVE
        self.mark_updated()

    def deactivate(self) -> None:
        """desativa entidade"""
        self.status = Status.INACTIVE
        self.mark_updated()

    @property
    def is_active(self) -> bool:
        return self.status == Status.ACTIVE