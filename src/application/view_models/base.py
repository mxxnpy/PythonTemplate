"""
Base ViewModels - modelos de resposta padrao
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """resposta padrao da API"""

    error: bool = Field(default=False, description="Indica se houve erro")
    error_message: str | None = Field(default=None, description="Mensagem de erro")
    result: T | None = Field(default=None, description="Resultado da operacao")

    @classmethod
    def success(cls, result: T) -> ApiResponse[T]:
        """cria resposta de sucesso"""
        return cls(error=False, error_message=None, result=result)

    @classmethod
    def fail(cls, message: str) -> ApiResponse[T]:
        """cria resposta de erro"""
        return cls(error=True, error_message=message, result=None)


class PaginatedResult(BaseModel, Generic[T]):
    """resultado paginado"""

    items: list[T] = Field(default_factory=list)
    total: int = Field(default=0)
    page: int = Field(default=1)
    page_size: int = Field(default=10)
    total_pages: int = Field(default=0)

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> PaginatedResult[T]:
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )


# alias para resposta paginada
PaginatedApiResponse = ApiResponse[PaginatedResult[T]]
