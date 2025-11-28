"""
Pipe Extensions - Composicao Fluente

Permite compor funcoes de forma fluente e legivel.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Pipe(Generic[T]):
    """wrapper para composicao fluente"""

    __slots__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def map(self, f: Callable[[T], R]) -> Pipe[R]:
        """transforma o valor"""
        return Pipe(f(self._value))

    def tap(self, f: Callable[[T], None]) -> Pipe[T]:
        """executa side effect sem alterar o valor"""
        f(self._value)
        return self

    def when(self, condition: bool, f: Callable[[T], T]) -> Pipe[T]:
        """aplica funcao se condicao for True"""
        return Pipe(f(self._value)) if condition else self

    def when_pred(self, predicate: Callable[[T], bool], f: Callable[[T], T]) -> Pipe[T]:
        """aplica funcao se predicado for True"""
        return Pipe(f(self._value)) if predicate(self._value) else self

    def unless(self, condition: bool, f: Callable[[T], T]) -> Pipe[T]:
        """aplica funcao se condicao for False"""
        return Pipe(f(self._value)) if not condition else self

    def filter(self, predicate: Callable[[T], bool], default: T) -> Pipe[T]:
        """retorna default se predicado for False"""
        return self if predicate(self._value) else Pipe(default)

    @property
    def value(self) -> T:
        """retorna o valor"""
        return self._value

    def __repr__(self) -> str:
        return f"Pipe({self._value!r})"


class AsyncPipe(Generic[T]):
    """wrapper para composicao fluente async"""

    __slots__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    async def map_async(self, f: Callable[[T], Awaitable[R]]) -> AsyncPipe[R]:
        """transforma o valor de forma async"""
        return AsyncPipe(await f(self._value))

    def map(self, f: Callable[[T], R]) -> AsyncPipe[R]:
        """transforma o valor de forma sync"""
        return AsyncPipe(f(self._value))

    async def tap_async(self, f: Callable[[T], Awaitable[None]]) -> AsyncPipe[T]:
        """executa side effect async sem alterar o valor"""
        await f(self._value)
        return self

    def tap(self, f: Callable[[T], None]) -> AsyncPipe[T]:
        """executa side effect sync sem alterar o valor"""
        f(self._value)
        return self

    @property
    def value(self) -> T:
        """retorna o valor"""
        return self._value


# funcoes helper para criar pipes
def pipe(value: T) -> Pipe[T]:
    """cria um Pipe com o valor"""
    return Pipe(value)


def async_pipe(value: T) -> AsyncPipe[T]:
    """cria um AsyncPipe com o valor"""
    return AsyncPipe(value)
