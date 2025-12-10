from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Info(BaseModel):
    count: int
    pages: int
    next: str | None
    prev: str | None


class PaginatedResponse(BaseModel, Generic[T]):
    info: Info
    results: list[T]
