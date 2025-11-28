"""
Result Pattern - Either Simplificado

Uma versao mais especifica do Either para Success/Failure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True, slots=True)
class Success(Generic[T]):
    """representa sucesso"""

    value: T

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class Failure:
    """representa falha"""

    error: str

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True


Result = Success[T] | Failure


# cria Success
def success(value: T) -> Result[T]:
    return Success(value)


# cria Failure
def failure(error: str) -> Result[T]:
    return Failure(error)


# transforma o valor se for Success
def map_result(result: Result[T], f: Callable[[T], U]) -> Result[U]:
    if isinstance(result, Success):
        return Success(f(result.value))
    return result


# encadeia operacoes que retornam Result
def bind_result(result: Result[T], f: Callable[[T], Result[U]]) -> Result[U]:
    if isinstance(result, Success):
        return f(result.value)
    return result


# retorna valor ou default
def get_or_default_result(result: Result[T], default: T) -> T:
    return result.value if isinstance(result, Success) else default


# trata ambos os casos
def match_result(
    result: Result[T],
    on_success: Callable[[T], U],
    on_failure: Callable[[str], U],
) -> U:
    if isinstance(result, Success):
        return on_success(result.value)
    return on_failure(result.error)

