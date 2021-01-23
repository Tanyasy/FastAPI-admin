from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 更新数据需要的数据类型
class PaymentBase(BaseModel):
    money: float = 0.00
    counter_party: Optional[str] = None
    payment: Optional[str] = None
    product_name: Optional[str] = None
    trade_sources: Optional[str] = ""
    trade_number: Optional[str] = ""


class PaymentCreate(PaymentBase):
    create_time: datetime = None
    update_time: datetime = None
    trade_type: Optional[str] = ""


class PaymentUpdate(PaymentBase):
    id: str
    user_id: Optional[str] = None
    trade_type: Optional[str] = ""


class PaymentInDB(PaymentBase):
    id: str
    create_time: datetime = None
    update_time: datetime = None
    trade_type: Optional[str] = ""
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class Payment(PaymentInDB):
    pass
