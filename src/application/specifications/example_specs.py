"""
Example Specifications - regras de validacao genericas
"""

from __future__ import annotations

from src.core import Specification
from src.domain.entities.example import Example
from src.domain.enums import Status


# specs para string
class NameNotEmptySpec(Specification[str]):
    """nome nao pode estar vazio"""

    def is_satisfied_by(self, entity: str) -> bool:
        return bool(entity and entity.strip())

    @property
    def error_message(self) -> str:
        return "Nome nao pode estar vazio"


# specs para numeros
class ValuePositiveSpec(Specification[int]):
    """valor deve ser positivo"""

    def is_satisfied_by(self, entity: int) -> bool:
        return entity > 0

    @property
    def error_message(self) -> str:
        return "Valor deve ser positivo"


class ValueInRangeSpec(Specification[int]):
    """valor deve estar no range"""

    def __init__(self, min_val: int, max_val: int):
        self._min = min_val
        self._max = max_val

    def is_satisfied_by(self, entity: int) -> bool:
        return self._min <= entity <= self._max

    @property
    def error_message(self) -> str:
        return f"Valor deve estar entre {self._min} e {self._max}"


# specs para entidade
class ExampleActiveSpec(Specification[Example]):
    """exemplo deve estar ativo"""

    def is_satisfied_by(self, entity: Example) -> bool:
        return entity.status == Status.ACTIVE

    @property
    def error_message(self) -> str:
        return "Exemplo deve estar ativo"


class ExampleNotDeletedSpec(Specification[Example]):
    """exemplo nao pode estar deletado"""

    def is_satisfied_by(self, entity: Example) -> bool:
        return entity.status != Status.DELETED

    @property
    def error_message(self) -> str:
        return "Exemplo nao pode estar deletado"


# specs compostas
def example_can_be_modified() -> Specification[Example]:
    """exemplo pode ser modificado se ativo e nao deletado"""
    return ExampleActiveSpec() & ExampleNotDeletedSpec()