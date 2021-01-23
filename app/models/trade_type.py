from sqlalchemy import Column, String, Integer

from app.db.base_class import Base


class TradeType(Base):

    type_name = Column(String(8), comment="交易类型名称")
    type_flag = Column(Integer, unique=True, comment="类型的唯一标记, 10以下为收入类型，10以上为消费类型")