from sqlalchemy import Column, String, Boolean, Float, ForeignKey

from app.db.base_class import Base


class Payment(Base):

    trade_number = Column(String(64), unique=True, comment="交易单号")
    money = Column(Float(10, 2), default=0.00, comment="金额")
    counter_party = Column(String(32), comment="交易方")
    payment = Column(String(2),  comment="收支")
    product_name = Column(String(64), comment="商品名称")
    trade_sources = Column(String(64), comment="交易来源")
    trade_type = Column(String(64), comment="消费类型")
    user_id = Column(String(64), ForeignKey("user.id"), comment="用户id")
    is_delete = Column(Boolean(), default=False, comment="删除标记")