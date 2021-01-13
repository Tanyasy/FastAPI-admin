from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_name(self, db_session: Session, *, user_name: str) -> Optional[User]:
        return db_session.query(User).filter(User.name == user_name).first()

    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            telephone=obj_in.telephone,
            name=obj_in.name,
            is_superuser=obj_in.is_superuser,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def authenticate(
            self, db_session: Session, *, user_name: str, password: str
    ) -> Optional[User]:
        user = self.get_by_name(db_session, user_name=user_name)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


# crud user实例对象，可以直接调用里面的方法
user = CRUDUser(User)
