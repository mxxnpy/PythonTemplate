"""
Tests for Specification Pattern
"""

from __future__ import annotations

import pytest

from src.core import Left, Right, Specification
from src.core.specification import (
    InRangeSpec,
    MaxLengthSpec,
    MinLengthSpec,
    NotEmptySpec,
    PositiveNumberSpec,
)


class TestSpecification:
    """testes para Specification pattern"""

    def test_not_empty_spec_valid(self) -> None:
        """NotEmptySpec deve passar para string nao vazia"""
        spec = NotEmptySpec("Nome")
        assert spec.is_satisfied_by("John")

    def test_not_empty_spec_invalid_empty(self) -> None:
        """NotEmptySpec deve falhar para string vazia"""
        spec = NotEmptySpec("Nome")
        assert not spec.is_satisfied_by("")

    def test_not_empty_spec_invalid_whitespace(self) -> None:
        """NotEmptySpec deve falhar para apenas espacos"""
        spec = NotEmptySpec("Nome")
        assert not spec.is_satisfied_by("   ")

    def test_min_length_spec_valid(self) -> None:
        """MinLengthSpec deve passar para string com tamanho minimo"""
        spec = MinLengthSpec(3, "Nome")
        assert spec.is_satisfied_by("John")

    def test_min_length_spec_invalid(self) -> None:
        """MinLengthSpec deve falhar para string muito curta"""
        spec = MinLengthSpec(3, "Nome")
        assert not spec.is_satisfied_by("Jo")

    def test_max_length_spec_valid(self) -> None:
        """MaxLengthSpec deve passar para string com tamanho maximo"""
        spec = MaxLengthSpec(10, "Nome")
        assert spec.is_satisfied_by("John")

    def test_max_length_spec_invalid(self) -> None:
        """MaxLengthSpec deve falhar para string muito longa"""
        spec = MaxLengthSpec(3, "Nome")
        assert not spec.is_satisfied_by("John")

    def test_positive_number_spec_valid(self) -> None:
        """PositiveNumberSpec deve passar para numero positivo"""
        spec = PositiveNumberSpec("Valor")
        assert spec.is_satisfied_by(10)

    def test_positive_number_spec_invalid_zero(self) -> None:
        """PositiveNumberSpec deve falhar para zero"""
        spec = PositiveNumberSpec("Valor")
        assert not spec.is_satisfied_by(0)

    def test_positive_number_spec_invalid_negative(self) -> None:
        """PositiveNumberSpec deve falhar para numero negativo"""
        spec = PositiveNumberSpec("Valor")
        assert not spec.is_satisfied_by(-5)

    def test_in_range_spec_valid(self) -> None:
        """InRangeSpec deve passar para valor no range"""
        spec = InRangeSpec(1, 100, "Idade")
        assert spec.is_satisfied_by(50)

    def test_in_range_spec_invalid_below(self) -> None:
        """InRangeSpec deve falhar para valor abaixo do range"""
        spec = InRangeSpec(1, 100, "Idade")
        assert not spec.is_satisfied_by(0)

    def test_in_range_spec_invalid_above(self) -> None:
        """InRangeSpec deve falhar para valor acima do range"""
        spec = InRangeSpec(1, 100, "Idade")
        assert not spec.is_satisfied_by(101)

    def test_and_composition_both_pass(self) -> None:
        """AND deve passar quando ambas specs passam"""
        spec1 = NotEmptySpec("Nome")
        spec2 = MinLengthSpec(2, "Nome")
        combined = spec1 & spec2
        assert combined.is_satisfied_by("John")

    def test_and_composition_one_fails(self) -> None:
        """AND deve falhar quando uma spec falha"""
        spec1 = NotEmptySpec("Nome")
        spec2 = MinLengthSpec(10, "Nome")
        combined = spec1 & spec2
        assert not combined.is_satisfied_by("John")

    def test_or_composition_one_passes(self) -> None:
        """OR deve passar quando uma spec passa"""
        spec1 = MinLengthSpec(10, "Nome")
        spec2 = NotEmptySpec("Nome")
        combined = spec1 | spec2
        assert combined.is_satisfied_by("John")

    def test_not_composition(self) -> None:
        """NOT deve inverter resultado"""
        spec = NotEmptySpec("Nome")
        inverted = ~spec
        assert inverted.is_satisfied_by("")
        assert not inverted.is_satisfied_by("John")

    def test_validate_returns_right_on_success(self) -> None:
        """validate deve retornar Right quando spec passa"""
        spec = NotEmptySpec("Nome")
        result = spec.validate("John")
        assert isinstance(result, Right)
        assert result.value == "John"

    def test_validate_returns_left_on_failure(self) -> None:
        """validate deve retornar Left quando spec falha"""
        spec = NotEmptySpec("Nome")
        result = spec.validate("")
        assert isinstance(result, Left)
        assert result.value.is_validation

