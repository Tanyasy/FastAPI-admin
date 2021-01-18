from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# 查询响应数据

# 插入数据库需要的数据

# 更新数据需要的数据类型
class PaymentBase(BaseModel):
    money: float = 0.00
    counter_party: Optional[str] = None
    payment: Optional[str] = None
    product_name: Optional[str] = None
    trade_sources: Optional[str] = ""


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    user_id: Optional[str] = None
    trade_type: Optional[str] = None


class PaymentInDB(PaymentBase):
    id: str
    create_time: datetime = None
    update_time: datetime = None
    trade_type: Optional[str] = ""
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class Payment(PaymentBase):
    pass
