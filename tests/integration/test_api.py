"""
Integration Tests for API
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api.app import app
from src.infrastructure.dependencies import get_example_repository


@pytest.fixture
def client() -> TestClient:
    """retorna cliente de teste"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_data() -> None:
    """limpa dados antes de cada teste"""
    repo = get_example_repository()
    repo.clear()


class TestHealthController:
    """testes para health controller"""

    def test_health_returns_healthy(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_ready_returns_ready(self, client: TestClient) -> None:
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


class TestExampleController:
    """testes para example controller"""

    def test_create_success(self, client: TestClient) -> None:
        response = client.post(
            "/examples",
            json={"name": "Test", "description": "Desc", "value": 10},
        )
        assert response.status_code == 201
        data = response.json()

        # verifica estrutura ApiResponse
        assert data["error"] is False
        assert data["error_message"] is None
        assert data["result"] is not None
        assert data["result"]["name"] == "Test"
        assert "id" in data["result"]

    def test_create_empty_name_fails(self, client: TestClient) -> None:
        response = client.post(
            "/examples",
            json={"name": "", "value": 10},
        )
        assert response.status_code == 422  # pydantic validation

    def test_create_duplicate_name_returns_error(self, client: TestClient) -> None:
        # cria primeiro
        client.post("/examples", json={"name": "Duplicate"})

        # tenta criar novamente
        response = client.post("/examples", json={"name": "Duplicate"})
        assert response.status_code == 201  # retorna 201 mas com erro no body
        data = response.json()
        assert data["error"] is True
        assert data["error_message"] is not None
        assert data["result"] is None

    def test_get_by_id_success(self, client: TestClient) -> None:
        # cria
        create_response = client.post(
            "/examples",
            json={"name": "Test"},
        )
        entity_id = create_response.json()["result"]["id"]

        # busca
        response = client.get(f"/examples/{entity_id}")
        assert response.status_code == 200
        data = response.json()

        assert data["error"] is False
        assert data["result"]["id"] == entity_id

    def test_get_by_id_not_found(self, client: TestClient) -> None:
        response = client.get("/examples/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    def test_update_success(self, client: TestClient) -> None:
        # cria
        create_response = client.post(
            "/examples",
            json={"name": "Original"},
        )
        entity_id = create_response.json()["result"]["id"]

        # atualiza
        response = client.put(
            f"/examples/{entity_id}",
            json={"name": "Updated"},
        )
        assert response.status_code == 200
        data = response.json()

        assert data["error"] is False
        assert data["result"]["name"] == "Updated"

    def test_delete_success(self, client: TestClient) -> None:
        # cria
        create_response = client.post(
            "/examples",
            json={"name": "ToDelete"},
        )
        entity_id = create_response.json()["result"]["id"]

        # deleta
        response = client.delete(f"/examples/{entity_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["error"] is False

        # confirma que nao existe mais
        get_response = client.get(f"/examples/{entity_id}")
        assert get_response.status_code == 404

    def test_list_empty(self, client: TestClient) -> None:
        response = client.get("/examples")
        assert response.status_code == 200
        data = response.json()

        assert data["error"] is False
        assert data["result"]["items"] == []
        assert data["result"]["total"] == 0

    def test_list_with_data(self, client: TestClient) -> None:
        # cria alguns
        for i in range(3):
            client.post("/examples", json={"name": f"Item {i}"})

        response = client.get("/examples")
        assert response.status_code == 200
        data = response.json()

        assert data["error"] is False
        assert len(data["result"]["items"]) == 3
        assert data["result"]["total"] == 3

    def test_list_pagination(self, client: TestClient) -> None:
        # cria 15 itens
        for i in range(15):
            client.post("/examples", json={"name": f"Item {i}"})

        response = client.get("/examples?page=2&page_size=5")
        assert response.status_code == 200
        data = response.json()

        assert data["error"] is False
        assert len(data["result"]["items"]) == 5
        assert data["result"]["total"] == 15
        assert data["result"]["page"] == 2
        assert data["result"]["total_pages"] == 3


class TestApiResponseStructure:
    """testes para estrutura padrao de resposta"""

    def test_success_response_structure(self, client: TestClient) -> None:
        response = client.post("/examples", json={"name": "Test"})
        data = response.json()

        # deve ter as 3 chaves
        assert "error" in data
        assert "error_message" in data
        assert "result" in data

    def test_error_response_structure(self, client: TestClient) -> None:
        # tenta criar duplicado para gerar erro
        client.post("/examples", json={"name": "Dup"})
        response = client.post("/examples", json={"name": "Dup"})
        data = response.json()

        assert data["error"] is True
        assert data["error_message"] is not None
        assert isinstance(data["error_message"], str)
