from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListCreate, TodoListUpdate
from app.crud.base import CRUDBase


class CRUDTodoList(CRUDBase[TodoList, TodoListCreate, TodoListUpdate]):

    def set_status(self, db_session: Session, *,  id: str, status: int) -> Optional[TodoList]:
        result = db_session.query(self.model).get(id)
        if result:
            result.status = status
            result.update_time = datetime.today()
            db_session.add(result)
            db_session.flush()
            db_session.commit()

        return result

    def get_multi_by_owner(
            self,
            db_session: Session,
            *,
            start_time: datetime = None,
            end_time: datetime = None,
            status: int = None,
            owner_id: str
    ) -> List[TodoList]:

        # 根据传入的参数有无添加不同的过滤条件
        filter_conditions: list = [TodoList.user_id == owner_id]
        if start_time:
            filter_conditions.append(TodoList.create_time >= str(start_time))

        if end_time:
            filter_conditions.append(TodoList.create_time <= str(end_time))

        if isinstance(status, int):
            filter_conditions.append(TodoList.status == status)

        # 默认按时间降序排序，要在limit和offset之前，不然会报错
        return (
            db_session.query(self.model)
                .filter(and_(*filter_conditions))
                .order_by(TodoList.create_time.desc())
                .all()
        )


# crud todo_list实例对象，可以直接调用里面的方法
todo_list = CRUDTodoList(TodoList)
