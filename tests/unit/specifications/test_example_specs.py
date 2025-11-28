"""
Tests for Example Specifications
"""

from __future__ import annotations

import pytest

from src.core import Left, Right
from src.application.specifications.example_specs import (
    ExampleActiveSpec,
    ExampleNotDeletedSpec,
    NameNotEmptySpec,
    ValueInRangeSpec,
    ValuePositiveSpec,
    example_can_be_modified,
)
from src.domain.entities.example import Example
from src.domain.enums import Status


class TestNameNotEmptySpec:
    """testes para NameNotEmptySpec"""

    def test_valid_name_satisfies(self) -> None:
        spec = NameNotEmptySpec()
        assert spec.is_satisfied_by("Test")

    def test_empty_name_fails(self) -> None:
        spec = NameNotEmptySpec()
        assert not spec.is_satisfied_by("")

    def test_whitespace_only_fails(self) -> None:
        spec = NameNotEmptySpec()
        assert not spec.is_satisfied_by("   ")


class TestValuePositiveSpec:
    """testes para ValuePositiveSpec"""

    def test_positive_value_satisfies(self) -> None:
        spec = ValuePositiveSpec()
        assert spec.is_satisfied_by(10)

    def test_zero_fails(self) -> None:
        spec = ValuePositiveSpec()
        assert not spec.is_satisfied_by(0)

    def test_negative_fails(self) -> None:
        spec = ValuePositiveSpec()
        assert not spec.is_satisfied_by(-5)


class TestValueInRangeSpec:
    """testes para ValueInRangeSpec"""

    def test_value_in_range_satisfies(self) -> None:
        spec = ValueInRangeSpec(1, 100)
        assert spec.is_satisfied_by(50)

    def test_value_at_min_satisfies(self) -> None:
        spec = ValueInRangeSpec(1, 100)
        assert spec.is_satisfied_by(1)

    def test_value_at_max_satisfies(self) -> None:
        spec = ValueInRangeSpec(1, 100)
        assert spec.is_satisfied_by(100)

    def test_value_below_range_fails(self) -> None:
        spec = ValueInRangeSpec(1, 100)
        assert not spec.is_satisfied_by(0)

    def test_value_above_range_fails(self) -> None:
        spec = ValueInRangeSpec(1, 100)
        assert not spec.is_satisfied_by(101)


class TestExampleActiveSpec:
    """testes para ExampleActiveSpec"""

    def test_active_entity_satisfies(self, active_entity: Example) -> None:
        spec = ExampleActiveSpec()
        assert spec.is_satisfied_by(active_entity)

    def test_pending_entity_fails(self, sample_entity: Example) -> None:
        spec = ExampleActiveSpec()
        assert not spec.is_satisfied_by(sample_entity)


class TestComposedSpecs:
    """testes para specs compostas"""

    def test_can_be_modified_active_satisfies(self, active_entity: Example) -> None:
        spec = example_can_be_modified()
        assert spec.is_satisfied_by(active_entity)

    def test_can_be_modified_deleted_fails(self, active_entity: Example) -> None:
        active_entity.status = Status.DELETED
        spec = example_can_be_modified()
        assert not spec.is_satisfied_by(active_entity)

    def test_validate_returns_either(self, active_entity: Example) -> None:
        spec = ExampleActiveSpec()
        result = spec.validate(active_entity)
        assert isinstance(result, Right)
        assert result.value == active_entity

