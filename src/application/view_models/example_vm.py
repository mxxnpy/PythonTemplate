"""
Example ViewModels - DTOs de request/response
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


# requests
class CreateExampleRequest(BaseModel):
    """request para criar exemplo"""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    value: int = Field(default=0, ge=0)


class UpdateExampleRequest(BaseModel):
    """request para atualizar exemplo"""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    value: int | None = Field(default=None, ge=0)


# responses
class ExampleResponse(BaseModel):
    """response de exemplo"""

    id: UUID
    name: str
    description: str
    value: int
    status: str
