from sqlalchemy import Column, String

from app.db.base_class import Base


class Role(Base):
    """
    角色类
    """
    name = Column(String(64), unique=True, index=True, comment="角色名")