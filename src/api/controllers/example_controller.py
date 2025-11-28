"""
Example Controller - endpoints de exemplo
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.application.handlers.example_handler import (
    CreateExampleCommand,
    GetByIdQuery,
    ListAllQuery,
    UpdateExampleCommand,
)
from src.application.view_models import (
    ApiResponse,
    CreateExampleRequest,
    ExampleResponse,
    PaginatedResult,
    UpdateExampleRequest,
)
from src.core import Left
from src.infrastructure.dependencies import ExampleHandlerDep

router = APIRouter(prefix="/examples", tags=["Examples"])


# helper para converter Either em ApiResponse
def to_api_response(result) -> ApiResponse:
    """converte Either para ApiResponse"""
    if isinstance(result, Left):
        error = result.value
        return ApiResponse.fail(error.first_message)
    return ApiResponse.success(result.value)


def unwrap_or_error(result) -> ApiResponse:
    """converte Either para ApiResponse, levanta HTTPException se erro critico"""
    if isinstance(result, Left):
        error = result.value
        if error.is_not_found:
            raise HTTPException(status_code=404, detail=error.first_message)
        return ApiResponse.fail(error.first_message)
    return ApiResponse.success(result.value)


@router.post("", response_model=ApiResponse[ExampleResponse], status_code=201)
async def create(
    request: CreateExampleRequest,
    handler: ExampleHandlerDep,
) -> ApiResponse[ExampleResponse]:
    """cria novo exemplo"""
    cmd = CreateExampleCommand(
        name=request.name,
        description=request.description,
        value=request.value,
    )
    result = await handler.create(cmd)
    return to_api_response(result)


@router.get("/{id}", response_model=ApiResponse[ExampleResponse])
async def get_by_id(
    id: UUID,
    handler: ExampleHandlerDep,
) -> ApiResponse[ExampleResponse]:
    """busca por id"""
    query = GetByIdQuery(id=id)
    result = await handler.get_by_id(query)
    return unwrap_or_error(result)


@router.put("/{id}", response_model=ApiResponse[ExampleResponse])
async def update(
    id: UUID,
    request: UpdateExampleRequest,
    handler: ExampleHandlerDep,
) -> ApiResponse[ExampleResponse]:
    """atualiza exemplo"""
    cmd = UpdateExampleCommand(
        id=id,
        name=request.name,
        description=request.description,
        value=request.value,
    )
    result = await handler.update(cmd)
    return unwrap_or_error(result)


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete(
    id: UUID,
    handler: ExampleHandlerDep,
) -> ApiResponse[None]:
    """deleta exemplo"""
    result = await handler.delete(id)
    return to_api_response(result)


@router.get("", response_model=ApiResponse[PaginatedResult[ExampleResponse]])
async def list_all(
    handler: ExampleHandlerDep,
    page: int = 1,
    page_size: int = 10,
) -> ApiResponse[PaginatedResult[ExampleResponse]]:
    """lista paginado"""
    query = ListAllQuery(page=page, page_size=page_size)
    result = await handler.list_all(query)
    return ApiResponse.success(result)
