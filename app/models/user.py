from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):

    name = Column(String(64), index=True)
    email = Column(String(32), unique=True, index=True)
    # int最大长度是11, 电话号码一般11位，所以如果用int类型存储会报错丢失。故一般用varchar(11)或nvarchar(11)保存
    tiktok_name = Column(String(32), index=True)
    hashed_password = Column(String(64))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    role_id = Column(String(64), ForeignKey("role.id"))

    role = relationship("Role", primaryjoin='User.role_id==foreign(Role.id)', passive_deletes=True, uselist=False)
