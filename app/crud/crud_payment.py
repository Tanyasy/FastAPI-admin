from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUBPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):

    def get_multi_by_owner(self, db_session: Session, *, skip=0, limit=100, owner_id: str) -> List[Payment]:
        return (
            db_session.query(self.model)
            .filter(Payment.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_multi_by_owner(self, db_session: Session, *, obj_in: List[PaymentCreate], owner_id: str) -> List[Payment]:
        obj_list_in_data = jsonable_encoder(obj_in)
        db_obj_list = [self.model(**obj_in_data, user_id=owner_id) for obj_in_data in obj_list_in_data]
        db_session.add(db_obj_list)
        db_session.commit()
        db_session.refresh(db_obj_list)
        return db_obj_list

payment = CRUBPayment(Payment)
