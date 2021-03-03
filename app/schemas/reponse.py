from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import TypeVar, List, Generic

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


class PageResponse2(GenericModel, Generic[T]):
    status: int
    count: int = 0
    data: List[T]
    total_page: int = 1