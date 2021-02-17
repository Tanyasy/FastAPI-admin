from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    # ...表示这个参数没有默认值，且必填
    name: str = Field(..., min_length=2, max_length=64)
    telephone: str = Field(..., regex="^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$")
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserBaseInDB(UserBase):
    id: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    # 暂时没必要
    # 密码强度正则，最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符: ^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$
    password: Optional[str] = Field(None, min_length=5, description="The password length must be greater than 5")


class UserUpdate(UserBaseInDB):
    password: Optional[str] = Field(None, min_length=5, description="The password length must be greater than 5")

class User(UserBaseInDB):
    role_name: str = ""

class UserInDB(UserBaseInDB):
    hashed_password: str