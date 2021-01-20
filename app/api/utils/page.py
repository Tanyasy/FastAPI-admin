from typing import List, TypeVar

T = TypeVar("T")


def pagination(recodes: List[T], current_page: int, limit: int):
    count: int = len(recodes)
    total_page: int = count // limit + 1
    if current_page == 0:
        current_page = 1
    if current_page >= total_page:
        current_page = total_page
    return {
        "status": 200,
        "count": count,
        "total_page": total_page,
        "data": recodes[(current_page-1)*limit: current_page*limit]
    }

