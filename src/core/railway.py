"""
Railway Oriented Programming

Encadeamento de operacoes onde qualquer falha "desvia" para a trilha de erro.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

from src.core.either import Either, Left, Right

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")


# encadeia operacoes sincronas
def then(
    either: Either[L, R],
    f: Callable[[R], Either[L, T]],
) -> Either[L, T]:
    """encadeia operacao que retorna Either"""
    if isinstance(either, Right):
        return f(either.value)
    return either  # type: ignore


# encadeia operacoes async
async def then_async(
    either: Either[L, R],
    f: Callable[[R], Awaitable[Either[L, T]]],
) -> Either[L, T]:
    """encadeia operacao async que retorna Either"""
    if isinstance(either, Right):
        return await f(either.value)
    return either  # type: ignore


# executa side effect sem alterar o valor
def tap(
    either: Either[L, R],
    f: Callable[[R], None],
) -> Either[L, R]:
    """executa funcao no valor sem alterar o Either"""
    if isinstance(either, Right):
        f(either.value)
    return either


# executa side effect async sem alterar o valor
async def tap_async(
    either: Either[L, R],
    f: Callable[[R], Awaitable[None]],
) -> Either[L, R]:
    """executa funcao async no valor sem alterar o Either"""
    if isinstance(either, Right):
        await f(either.value)
    return either


# tenta executar e captura excecao
def try_catch(
    f: Callable[[], T],
    on_error: Callable[[Exception], L],
) -> Either[L, T]:
    """executa funcao e captura excecao convertendo para Left"""
    try:
        return Right(f())
    except Exception as e:
        return Left(on_error(e))


# tenta executar async e captura excecao
async def try_catch_async(
    f: Callable[[], Awaitable[T]],
    on_error: Callable[[Exception], L],
) -> Either[L, T]:
    """executa funcao async e captura excecao convertendo para Left"""
    try:
        return Right(await f())
    except Exception as e:
        return Left(on_error(e))


# combina multiplos Eithers
def combine_all(
    *eithers: Either[L, R],
) -> Either[L, tuple[R, ...]]:
    """combina multiplos Eithers em um unico Either de tupla"""
    results: list[R] = []
    for e in eithers:
        if isinstance(e, Left):
            return e  # type: ignore
        results.append(e.value)
    return Right(tuple(results))


# executa condicional
def when(
    condition: bool,
    on_true: Callable[[], Either[L, R]],
    on_false: Callable[[], Either[L, R]],
) -> Either[L, R]:
    """executa funcao baseado na condicao"""
    return on_true() if condition else on_false()


# garante valor ou retorna erro
def ensure(
    value: R,
    predicate: Callable[[R], bool],
    error: L,
) -> Either[L, R]:
    """retorna Right se predicado for True, Left caso contrario"""
    return Right(value) if predicate(value) else Left(error)
