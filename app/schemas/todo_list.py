from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TodoListBase(BaseModel):
    # ...表示这个参数没有默认值，且必填
    desc: str = Field(..., min_length=2, max_length=64)
    title: str = Field(..., regex="^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$")
    parent_id: Optional[EmailStr] = None
    user_id: Optional[bool] = True



class TodoListBaseInDB(TodoListBase):
    id: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True


class TodoListCreate(TodoListBase):
    # 暂时没必要
    # 密码强度正则，最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符: ^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$
    password: Optional[str] = Field(None, min_length=5, description="The password length must be greater than 5")


class TodoListUpdate(TodoListBaseInDB):
    password: Optional[str] = Field(None, min_length=5, description="The password length must be greater than 5")
    role_id: str = None


class TodoList(TodoListBaseInDB):
    role_name: str = ""

class TodoListInDB(TodoListBaseInDB):
    hashed_password: str