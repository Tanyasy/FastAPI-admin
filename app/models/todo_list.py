from sqlalchemy import Column, String, Boolean, ForeignKey, Text, Integer, SmallInteger, BigInteger
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class TodoList(Base):
    """待办事项模型类"""
    desc = Column(Text(), default="", comment="描述")
    title = Column(String(64), index=True, default="", comment="标题")
    parent_id = Column(String(32), default=None, index=True, comment="上级任务id")
    user_id = Column(String(32), default=None, index=True, comment="用户id")
    project_id = Column(String(32), default=None, index=True, comment="项目（类型）id")
    priority = Column(SmallInteger(), default=1, comment="优先级")
    status = Column(SmallInteger(), default=0, comment="状态标记，0进行中|2已完成")
    sort_value = Column(BigInteger(), default=None, comment="排序标记")

    is_delete = Column(Boolean(), default=False)

"""
id:   varchar32  字段
projectId： varchar32 任务集合，可以先当做一个分类，外键
parentId: varchar32
title:  varchar256 标题
desc: text 描述
userId：varchar32 创建人
priority: int 优先级
focusSummaries： list 番茄钟专注数据
status: int 0|1|2  
repeatTaskId: 如果有子任务
sortvalue
reminder
createTime :date

updateTime: date
"""