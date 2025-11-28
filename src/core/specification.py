"""
Specification Pattern - Regras de Negocio Encapsulaveis

Permite compor regras de negocio de forma declarativa.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from src.core.either import Either, Left, Right
from src.core.error_result import ErrorResult

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """classe base para specifications"""

    @abstractmethod
    def is_satisfied_by(self, entity: T) -> bool:
        """verifica se entidade satisfaz a especificacao"""
        pass

    @property
    @abstractmethod
    def error_message(self) -> str:
        """mensagem de erro quando nao satisfeito"""
        pass

    def validate(self, entity: T) -> Either[ErrorResult, T]:
        """valida e retorna Either"""
        if self.is_satisfied_by(entity):
            return Right(entity)
        return Left(ErrorResult.validation(self.error_message))

    def and_(self, other: Specification[T]) -> Specification[T]:
        """combina com AND"""
        return AndSpec(self, other)

    def or_(self, other: Specification[T]) -> Specification[T]:
        """combina com OR"""
        return OrSpec(self, other)

    def not_(self) -> Specification[T]:
        """nega a especificacao"""
        return NotSpec(self)

    def __and__(self, other: Specification[T]) -> Specification[T]:
        """permite usar & para combinar"""
        return self.and_(other)

    def __or__(self, other: Specification[T]) -> Specification[T]:
        """permite usar | para combinar"""
        return self.or_(other)

    def __invert__(self) -> Specification[T]:
        """permite usar ~ para negar"""
        return self.not_()


@dataclass
class AndSpec(Specification[T]):
    """combina duas specs com AND"""

    left: Specification[T]
    right: Specification[T]

    def is_satisfied_by(self, entity: T) -> bool:
        return self.left.is_satisfied_by(entity) and self.right.is_satisfied_by(entity)

    @property
    def error_message(self) -> str:
        # retorna erro do primeiro que falhar
        return self.left.error_message

    def validate(self, entity: T) -> Either[ErrorResult, T]:
        """valida ambas as specs e acumula erros"""
        left_result = self.left.is_satisfied_by(entity)
        right_result = self.right.is_satisfied_by(entity)

        if left_result and right_result:
            return Right(entity)

        errors: list[str] = []
        if not left_result:
            errors.append(self.left.error_message)
        if not right_result:
            errors.append(self.right.error_message)

        return Left(ErrorResult.validation_list(errors))


@dataclass
class OrSpec(Specification[T]):
    """combina duas specs com OR"""

    left: Specification[T]
    right: Specification[T]

    def is_satisfied_by(self, entity: T) -> bool:
        return self.left.is_satisfied_by(entity) or self.right.is_satisfied_by(entity)

    @property
    def error_message(self) -> str:
        return f"{self.left.error_message} ou {self.right.error_message}"


@dataclass
class NotSpec(Specification[T]):
    """nega uma spec"""

    spec: Specification[T]

    def is_satisfied_by(self, entity: T) -> bool:
        return not self.spec.is_satisfied_by(entity)

    @property
    def error_message(self) -> str:
        return f"Nao: {self.spec.error_message}"


# specs utilitarias comuns
class NotEmptySpec(Specification[str]):
    """valida se string nao esta vazia"""

    def __init__(self, field_name: str = "Campo"):
        self._field_name = field_name

    def is_satisfied_by(self, entity: str) -> bool:
        return bool(entity and entity.strip())

    @property
    def error_message(self) -> str:
        return f"{self._field_name} nao pode estar vazio"


class MinLengthSpec(Specification[str]):
    """valida tamanho minimo"""

    def __init__(self, min_length: int, field_name: str = "Campo"):
        self._min_length = min_length
        self._field_name = field_name

    def is_satisfied_by(self, entity: str) -> bool:
        return len(entity) >= self._min_length

    @property
    def error_message(self) -> str:
        return f"{self._field_name} deve ter no minimo {self._min_length} caracteres"


class MaxLengthSpec(Specification[str]):
    """valida tamanho maximo"""

    def __init__(self, max_length: int, field_name: str = "Campo"):
        self._max_length = max_length
        self._field_name = field_name

    def is_satisfied_by(self, entity: str) -> bool:
        return len(entity) <= self._max_length

    @property
    def error_message(self) -> str:
        return f"{self._field_name} deve ter no maximo {self._max_length} caracteres"


class PositiveNumberSpec(Specification[int | float]):
    """valida se numero e positivo"""

    def __init__(self, field_name: str = "Valor"):
        self._field_name = field_name

    def is_satisfied_by(self, entity: int | float) -> bool:
        return entity > 0

    @property
    def error_message(self) -> str:
        return f"{self._field_name} deve ser positivo"


class InRangeSpec(Specification[int | float]):
    """valida se numero esta no range"""

    def __init__(self, min_val: int | float, max_val: int | float, field_name: str = "Valor"):
        self._min = min_val
        self._max = max_val
        self._field_name = field_name

    def is_satisfied_by(self, entity: int | float) -> bool:
        return self._min <= entity <= self._max

    @property
    def error_message(self) -> str:
        return f"{self._field_name} deve estar entre {self._min} e {self._max}"