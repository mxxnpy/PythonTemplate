# view models (DTOs de request/response)
from src.application.view_models.base import ApiResponse, PaginatedResult
from src.application.view_models.example_vm import (
    CreateExampleRequest,
    ExampleResponse,
    UpdateExampleRequest,
)

__all__ = [
    "ApiResponse",
    "PaginatedResult",
    "CreateExampleRequest",
    "UpdateExampleRequest",
    "ExampleResponse",
]
