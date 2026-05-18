from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

T = TypeVar("T")


class AccessDataRequest(BaseModel):
    member_id: UUID | None
    server_id: UUID
    permission_mask: int
    restriction_mask: int


class PaginationRequest(BaseModel):
    page: int | None = None
    page_size: int = 50


class ResponseMessage(BaseModel, Generic[T]):
    status: int
    message: T


class ErrorResponse(BaseModel):
    message: str


class StatusResponse(BaseModel):
    status: str = Field(default="ok")
