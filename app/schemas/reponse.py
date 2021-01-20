from pydantic import BaseModel
from typing import TypeVar, List

T = TypeVar("T")


class Response(BaseModel):
    status: int
    msg: str = ""
    data: List[T]
    total: int = 0


class PageResponse(BaseModel):
    status: int
    count: int = 0
    data: List[T]
    total_page: int = 1