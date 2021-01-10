import uuid
import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr



class CustomBase(object):
    """
    自动生成表名，为类名的小写
    """
    # 为基类增加Column不能直接定义，只能通过@declared_attr修饰符定义
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


    @declared_attr
    def id(self):
        return  Column(String(32),primary_key=True,default=uuid.uuid4().hex)#唯一性的UUID

    @declared_attr
    def create_time(self):
        return Column(DateTime, default=datetime.datetime.now, comment='创建时间')

    @declared_attr
    def update_time(self):
        return Column(DateTime, default=datetime.datetime.now, comment='修改时间')


Base = declarative_base(cls=CustomBase)