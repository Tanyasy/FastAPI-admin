from sqlalchemy.orm import Session
from typing import Optional

from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListCreate, TodoListUpdate
from app.crud.base import CRUDBase


class CRUDTodoList(CRUDBase[TodoList, TodoListCreate, TodoListUpdate]):

    pass
    # def get_by_name(self, db_session: Session, *, todo_list_name: str) -> Optional[TodoList]:
    #     return db_session.query(todo_list).filter(todo_list.name == todo_list_name).first()
    #
    # def create(self, db_session: Session, *, obj_in: TodoListCreate) -> TodoList:
    #     db_obj = todo_list(
    #         email=obj_in.email,
    #         hashed_password=get_password_hash(obj_in.password),
    #         telephone=obj_in.telephone,
    #         name=obj_in.name,
    #         is_supertodo_list=obj_in.is_supertodo_list,
    #     )
    #     db_session.add(db_obj)
    #     db_session.commit()
    #     db_session.refresh(db_obj)
    #     return db_obj
    #
    # def authenticate(
    #         self, db_session: Session, *, todo_list_name: str, password: str
    # ) -> Optional[todo_list]:
    #     todo_list = self.get_by_name(db_session, todo_list_name=todo_list_name)
    #     if not todo_list:
    #         return None
    #     if not verify_password(password, todo_list.hashed_password):
    #         return None
    #     return todo_list
    #
    # def is_active(self, todo_list: todo_list) -> bool:
    #     return todo_list.is_active


# crud todo_list实例对象，可以直接调用里面的方法
todo_list = CRUDTodoList(TodoList)
