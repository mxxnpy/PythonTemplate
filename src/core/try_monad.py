"""
Try Monad - Encapsula Excecoes

Converte codigo que lanca excecao para Either.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, TypeVar

from src.core.either import Either, Left, Right
from src.core.error_result import ErrorResult

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True, slots=True)
class TrySuccess(Generic[T]):
    """representa execucao bem sucedida"""

    value: T

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class TryFailure:
    """representa falha com excecao"""

    exception: Exception

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True


Try = TrySuccess[T] | TryFailure


# executa funcao e captura excecao
def try_of(f: Callable[[], T]) -> Try[T]:
    """executa funcao e retorna Try"""
    try:
        return TrySuccess(f())
    except Exception as e:
        return TryFailure(e)


# executa funcao async e captura excecao
async def try_of_async(f: Callable[[], Awaitable[T]]) -> Try[T]:
    """executa funcao async e retorna Try"""
    try:
        return TrySuccess(await f())
    except Exception as e:
        return TryFailure(e)


# transforma valor se sucesso
def map_try(t: Try[T], f: Callable[[T], U]) -> Try[U]:
    """transforma o valor se Try for sucesso"""
    if isinstance(t, TrySuccess):
        return try_of(lambda: f(t.value))
    return t


# encadeia operacoes Try
def bind_try(t: Try[T], f: Callable[[T], Try[U]]) -> Try[U]:
    """encadeia operacao que retorna Try"""
    if isinstance(t, TrySuccess):
        return f(t.value)
    return t


# converte Try para Either
def to_either(t: Try[T]) -> Either[ErrorResult, T]:
    """converte Try para Either com ErrorResult"""
    if isinstance(t, TrySuccess):
        return Right(t.value)
    return Left(ErrorResult.from_exception(t.exception))


# converte Try para Either com erro customizado
def to_either_with(t: Try[T], on_error: Callable[[Exception], ErrorResult]) -> Either[ErrorResult, T]:
    """converte Try para Either com funcao de erro customizada"""
    if isinstance(t, TrySuccess):
        return Right(t.value)
    return Left(on_error(t.exception))


# retorna valor ou default
def get_or_default_try(t: Try[T], default: T) -> T:
    """retorna valor ou default se falha"""
    return t.value if isinstance(t, TrySuccess) else default


# retorna valor ou executa funcao
def get_or_else_try(t: Try[T], on_failure: Callable[[Exception], T]) -> T:
    """retorna valor ou executa funcao se falha"""
    if isinstance(t, TrySuccess):
        return t.value
    return on_failure(t.exception)


# recupera de falha
def recover(t: Try[T], f: Callable[[Exception], T]) -> Try[T]:
    """tenta recuperar de falha"""
    if isinstance(t, TryFailure):
        return try_of(lambda: f(t.exception))
    return t


# recupera de falha com Try
def recover_with(t: Try[T], f: Callable[[Exception], Try[T]]) -> Try[T]:
    """tenta recuperar de falha com outra operacao Try"""
    if isinstance(t, TryFailure):
        return f(t.exception)
    return t

