from pydantic import BaseModel, Field
from datetime import datetime


class TradeTypeBase(BaseModel):

    type_name: str = Field(..., max_length=8)
    type_flag: int = Field(..., gt=0, lt=100)


class TradeTypeCreate(TradeTypeBase):
    pass


class TradeTypeUpdate(TradeTypeBase):
    update_time: datetime = datetime.today()


class TradeType(TradeTypeBase):
    id: str
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
