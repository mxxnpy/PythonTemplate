"""
Either Monad - Sucesso ou Erro

O Either representa um valor que pode ser uma de duas coisas:
- Left -> Convencionalmente representa erro/falha
- Right -> Convencionalmente representa sucesso

"Right is right" (Right esta certo/correto)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Left(Generic[L]):
    """representa erro/falha"""

    value: L

    @property
    def is_left(self) -> bool:
        return True

    @property
    def is_right(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class Right(Generic[R]):
    """representa sucesso"""

    value: R

    @property
    def is_left(self) -> bool:
        return False

    @property
    def is_right(self) -> bool:
        return True


Either = Union[Left[L], Right[R]]


# trata ambos os casos e retorna um valor
def match(
    either: Either[L, R],
    on_left: Callable[[L], T],
    on_right: Callable[[R], T],
) -> T:
    if isinstance(either, Left):
        return on_left(either.value)
    return on_right(either.value)


# transforma o valor de sucesso (Right)
def map_right(either: Either[L, R], f: Callable[[R], T]) -> Either[L, T]:
    if isinstance(either, Right):
        return Right(f(either.value))
    return either  # type: ignore


# encadeia operacoes que tambem retornam Either
def bind(either: Either[L, R], f: Callable[[R], Either[L, T]]) -> Either[L, T]:
    if isinstance(either, Right):
        return f(either.value)
    return either  # type: ignore

