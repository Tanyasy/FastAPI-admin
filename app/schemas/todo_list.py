from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TodoListBase(BaseModel):
    # ...表示这个参数没有默认值，且必填
    desc: str = ""
    title: str = ""
    parent_id: str = None


class TodoListCreate(TodoListBase):
    pass


class TodoListUpdate(TodoListBase):
    project_id: Optional[str] = None
    priority: Optional[int] = 1
    status: Optional[int] = 0


class TodoListBaseInDB(TodoListUpdate):
    id: str = None
    create_time: datetime = None
    update_time: datetime = None
    user_id: Optional[str] = None
    sort_value: Optional[int] = None
    is_delete: Optional[bool] = False

    class Config:
        orm_mode = True


class TodoList(TodoListBaseInDB):
    pass
