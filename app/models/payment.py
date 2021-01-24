from sqlalchemy import Column, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Payment(Base):

    trade_number = Column(String(64), unique=True, comment="交易单号")
    money = Column(Float(10, 2), default=0.00, comment="金额")
    counter_party = Column(String(32), comment="交易方")
    payment = Column(String(2),  comment="收支")
    product_name = Column(String(64), comment="商品名称")
    trade_sources = Column(String(64), comment="交易来源")
    trade_type = Column(String(64), ForeignKey("tradetype.id"), comment="消费类型")
    user_id = Column(String(64), ForeignKey("user.id"), comment="用户id")
    is_delete = Column(Boolean(), default=False, comment="删除标记")
    # relationship()的参数中有一个称为backref()的relationship()的子函数，反向提供详细的信息, 即在users中添加User对应的Address对象的集合，保存在User.addresses中
    # passive_deletes:默认为false，删除子表数据会级联删除父表数据，设置为True，则不会进行级联删除
    type = relationship("TradeType", primaryjoin='Payment.trade_type==foreign(TradeType.id)', passive_deletes=True, uselist=False)