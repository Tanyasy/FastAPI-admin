from sqlalchemy import Column, String, Boolean

from app.db.base_class import Base


class User(Base):

    name = Column(String(64), index=True)
    email = Column(String(32), unique=True, index=True)
    # int最大长度是11, 电话号码一般11位，所以如果用int类型存储会报错丢失。故一般用varchar(11)或nvarchar(11)保存
    telephone = Column(String(11), index=True)
    hashed_password = Column(String(64))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

