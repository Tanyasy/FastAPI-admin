from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUBPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):

    def get_multi_by_owner(self, db_session: Session, *, start_time: datetime=None, end_time: datetime=None, owner_id: str) -> List[Payment]:
        if start_time:
            return (
                db_session.query(self.model)
                    .filter(and_(Payment.user_id == owner_id, Payment.create_time.between(str(start_time), str(end_time))))
                    .order_by(Payment.create_time.desc())
                    .all()
            )
        else:
            # 默认按时间降序排序，要在limit和offset之前，不然会报错
            return (
                db_session.query(self.model)
                .filter(and_(Payment.user_id == owner_id, Payment.create_time <= str(end_time)))
                .order_by(Payment.create_time.desc())
                .all()
            )

    def create_multi_by_owner(self, db_session: Session, *, obj_in: List[PaymentCreate], owner_id: str) -> List[Payment]:
        obj_list_in_data = jsonable_encoder(obj_in)
        db_obj_list = [self.model(**obj_in_data, user_id=owner_id) for obj_in_data in obj_list_in_data]
        db_session.add_all(db_obj_list)
        db_session.flush()
        db_session.commit()
        return db_obj_list

payment = CRUBPayment(Payment)
