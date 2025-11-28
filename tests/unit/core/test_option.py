"""
Tests for Option Monad
"""

from __future__ import annotations

import pytest

from src.core import Nothing, Some, from_nullable, get_or_default
from src.core.option import bind_option, map_option, match_option, to_either
from src.core import ErrorResult


class TestOption:
    """testes para Option monad"""

    def test_some_is_some(self) -> None:
        """Some deve ter is_some True"""
        result = Some(42)
        assert result.is_some
        assert not result.is_none

    def test_nothing_is_none(self) -> None:
        """Nothing deve ter is_none True"""
        result = Nothing()
        assert result.is_none
        assert not result.is_some

    def test_from_nullable_with_value(self) -> None:
        """from_nullable deve retornar Some para valor existente"""
        result = from_nullable("hello")
        assert isinstance(result, Some)
        assert result.value == "hello"

    def test_from_nullable_with_none(self) -> None:
        """from_nullable deve retornar Nothing para None"""
        result = from_nullable(None)
        assert isinstance(result, Nothing)

    def test_get_or_default_with_some(self) -> None:
        """get_or_default deve retornar valor para Some"""
        result = Some(42)
        assert get_or_default(result, 0) == 42

    def test_get_or_default_with_nothing(self) -> None:
        """get_or_default deve retornar default para Nothing"""
        result = Nothing()
        assert get_or_default(result, 0) == 0

    def test_map_option_with_some(self) -> None:
        """map_option deve transformar valor de Some"""
        result = Some(10)
        mapped = map_option(result, lambda x: x * 2)
        assert isinstance(mapped, Some)
        assert mapped.value == 20

    def test_map_option_with_nothing(self) -> None:
        """map_option deve retornar Nothing para Nothing"""
        result = Nothing()
        mapped = map_option(result, lambda x: x * 2)
        assert isinstance(mapped, Nothing)

    def test_bind_option_chains(self) -> None:
        """bind_option deve encadear operacoes"""
        result = Some(10)

        def safe_divide(x: int):
            return Some(x // 2) if x > 0 else Nothing()

        chained = bind_option(result, safe_divide)
        assert isinstance(chained, Some)
        assert chained.value == 5

    def test_to_either_with_some(self) -> None:
        """to_either deve retornar Right para Some"""
        result = Some(42)
        either = to_either(result, ErrorResult.not_found("nao encontrado"))
        assert either.is_right
        assert either.value == 42

    def test_to_either_with_nothing(self) -> None:
        """to_either deve retornar Left para Nothing"""
        result = Nothing()
        either = to_either(result, ErrorResult.not_found("nao encontrado"))
        assert either.is_left
        assert either.value.is_not_found

    def test_match_option_with_some(self) -> None:
        """match_option deve executar on_some para Some"""
        result = Some(42)
        output = match_option(
            result,
            on_some=lambda v: f"valor: {v}",
            on_none=lambda: "vazio",
        )
        assert output == "valor: 42"

    def test_match_option_with_nothing(self) -> None:
        """match_option deve executar on_none para Nothing"""
        result = Nothing()
        output = match_option(
            result,
            on_some=lambda v: f"valor: {v}",
            on_none=lambda: "vazio",
        )
        assert output == "vazio"

