from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from app.schemas.permission import Permission


class RoleBase(BaseModel):

    name: str = Field(..., max_length=128)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    update_time: datetime = datetime.today()


class Role(RoleBase):
    id: str
    create_time: datetime
    update_time: datetime
    permissions: List[Permission] = None

    class Config:
        orm_mode = True