"""
Tests for ApiResponse
"""

from __future__ import annotations

import pytest

from src.application.view_models import ApiResponse, PaginatedResult


class TestApiResponse:
    """testes para ApiResponse"""

    def test_success_creates_valid_response(self) -> None:
        response = ApiResponse.success({"id": 1, "name": "Test"})

        assert response.error is False
        assert response.error_message is None
        assert response.result == {"id": 1, "name": "Test"}

    def test_fail_creates_error_response(self) -> None:
        response = ApiResponse.fail("Algo deu errado")

        assert response.error is True
        assert response.error_message == "Algo deu errado"
        assert response.result is None

    def test_success_with_none_result(self) -> None:
        response = ApiResponse.success(None)

        assert response.error is False
        assert response.error_message is None
        assert response.result is None

    def test_response_is_serializable(self) -> None:
        response = ApiResponse.success({"data": "value"})
        json_data = response.model_dump()

        assert json_data["error"] is False
        assert json_data["error_message"] is None
        assert json_data["result"] == {"data": "value"}


class TestPaginatedResult:
    """testes para PaginatedResult"""

    def test_create_calculates_total_pages(self) -> None:
        result = PaginatedResult.create(
            items=["a", "b", "c"],
            total=10,
            page=1,
            page_size=3,
        )

        assert result.items == ["a", "b", "c"]
        assert result.total == 10
        assert result.page == 1
        assert result.page_size == 3
        assert result.total_pages == 4  # ceil(10/3) = 4

    def test_create_with_exact_division(self) -> None:
        result = PaginatedResult.create(
            items=["a", "b"],
            total=10,
            page=1,
            page_size=5,
        )

        assert result.total_pages == 2  # 10/5 = 2

    def test_create_with_empty_items(self) -> None:
        result = PaginatedResult.create(
            items=[],
            total=0,
            page=1,
            page_size=10,
        )

        assert result.items == []
        assert result.total == 0
        assert result.total_pages == 0

    def test_create_with_zero_page_size(self) -> None:
        result = PaginatedResult.create(
            items=[],
            total=10,
            page=1,
            page_size=0,
        )

        assert result.total_pages == 0

    def test_paginated_in_api_response(self) -> None:
        paginated = PaginatedResult.create(
            items=[{"id": 1}, {"id": 2}],
            total=2,
            page=1,
            page_size=10,
        )
        response = ApiResponse.success(paginated)

        assert response.error is False
        assert response.result.items == [{"id": 1}, {"id": 2}]
        assert response.result.total == 2

