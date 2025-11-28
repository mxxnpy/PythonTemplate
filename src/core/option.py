"""
Option Monad - Valores Opcionais

Representa um valor que pode ou nao existir (alternativa ao null).
- Some -> Valor existe
- Nothing -> Valor nao existe
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

from src.core.either import Either, Left, Right

T = TypeVar("T")
U = TypeVar("U")
L = TypeVar("L")


@dataclass(frozen=True, slots=True)
class Some(Generic[T]):
    """representa valor existente"""

    value: T

    @property
    def is_some(self) -> bool:
        return True

    @property
    def is_none(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class Nothing:
    """representa ausencia de valor"""

    @property
    def is_some(self) -> bool:
        return False

    @property
    def is_none(self) -> bool:
        return True


Option = Union[Some[T], Nothing]


# cria Option a partir de valor nullable
def from_nullable(value: T | None) -> Option[T]:
    return Some(value) if value is not None else Nothing()


# retorna valor ou default
def get_or_default(option: Option[T], default: T) -> T:
    return option.value if isinstance(option, Some) else default


# transforma o valor se existir
def map_option(option: Option[T], f: Callable[[T], U]) -> Option[U]:
    if isinstance(option, Some):
        return Some(f(option.value))
    return Nothing()


# encadeia operacoes que retornam Option
def bind_option(option: Option[T], f: Callable[[T], Option[U]]) -> Option[U]:
    if isinstance(option, Some):
        return f(option.value)
    return Nothing()


# converte Option para Either
def to_either(option: Option[T], left_value: L) -> Either[L, T]:
    if isinstance(option, Some):
        return Right(option.value)
    return Left(left_value)


# trata ambos os casos
def match_option(
    option: Option[T],
    on_some: Callable[[T], U],
    on_none: Callable[[], U],
) -> U:
    if isinstance(option, Some):
        return on_some(option.value)
    return on_none()

