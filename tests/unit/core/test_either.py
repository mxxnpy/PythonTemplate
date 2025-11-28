"""
Tests for Either Monad
"""

from __future__ import annotations

import pytest

from src.core import Either, Left, Right, bind, map_right, match


class TestEither:
    """testes para Either monad"""

    def test_right_is_right(self) -> None:
        """Right deve ter is_right True"""
        result: Either[str, int] = Right(42)
        assert result.is_right
        assert not result.is_left

    def test_left_is_left(self) -> None:
        """Left deve ter is_left True"""
        result: Either[str, int] = Left("erro")
        assert result.is_left
        assert not result.is_right

    def test_match_right(self) -> None:
        """match deve executar funcao right para Right"""
        result: Either[str, int] = Right(42)
        output = match(
            result,
            on_left=lambda e: f"erro: {e}",
            on_right=lambda v: f"valor: {v}",
        )
        assert output == "valor: 42"

    def test_match_left(self) -> None:
        """match deve executar funcao left para Left"""
        result: Either[str, int] = Left("falhou")
        output = match(
            result,
            on_left=lambda e: f"erro: {e}",
            on_right=lambda v: f"valor: {v}",
        )
        assert output == "erro: falhou"

    def test_map_right_transforms_value(self) -> None:
        """map_right deve transformar valor de Right"""
        result: Either[str, int] = Right(10)
        mapped = map_right(result, lambda x: x * 2)
        assert isinstance(mapped, Right)
        assert mapped.value == 20

    def test_map_right_ignores_left(self) -> None:
        """map_right deve ignorar Left"""
        result: Either[str, int] = Left("erro")
        mapped = map_right(result, lambda x: x * 2)
        assert isinstance(mapped, Left)
        assert mapped.value == "erro"

    def test_bind_chains_operations(self) -> None:
        """bind deve encadear operacoes"""
        result: Either[str, int] = Right(10)

        def double_if_positive(x: int) -> Either[str, int]:
            return Right(x * 2) if x > 0 else Left("deve ser positivo")

        chained = bind(result, double_if_positive)
        assert isinstance(chained, Right)
        assert chained.value == 20

    def test_bind_stops_at_left(self) -> None:
        """bind deve parar quando encontrar Left"""
        result: Either[str, int] = Left("erro inicial")

        def should_not_run(x: int) -> Either[str, int]:
            raise AssertionError("nao deveria executar")

        chained = bind(result, should_not_run)
        assert isinstance(chained, Left)
        assert chained.value == "erro inicial"

    def test_pipeline_success(self) -> None:
        """pipeline de sucesso deve processar todos os passos"""

        def step1(x: int) -> Either[str, int]:
            return Right(x + 1)

        def step2(x: int) -> Either[str, int]:
            return Right(x * 2)

        def step3(x: int) -> Either[str, str]:
            return Right(f"resultado: {x}")

        result = bind(bind(Right(5), step1), step2)
        final = bind(result, step3)

        assert isinstance(final, Right)
        assert final.value == "resultado: 12"

    def test_pipeline_fails_at_middle(self) -> None:
        """pipeline deve parar no primeiro erro"""

        def step1(x: int) -> Either[str, int]:
            return Right(x + 1)

        def step2(x: int) -> Either[str, int]:
            return Left("falhou no step2")

        def step3(x: int) -> Either[str, str]:
            raise AssertionError("nao deveria executar")

        result = bind(bind(Right(5), step1), step2)

        assert isinstance(result, Left)
        assert result.value == "falhou no step2"

