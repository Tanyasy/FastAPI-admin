from pydantic import BaseModel, Field
from datetime import datetime


class PermissionBase(BaseModel):

    name: str = Field(..., max_length=128)
    codename: str = Field(..., max_length=128)


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    id: str
    update_time: datetime = datetime.today()


class Permission(PermissionBase):
    id: str
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True