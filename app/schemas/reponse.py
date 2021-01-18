from pydantic import BaseModel
from typing import TypeVar, List

T = TypeVar("T")


class Response(BaseModel):
    status: int
    msg: str = ""
    data: List[T]
    total: int = 0