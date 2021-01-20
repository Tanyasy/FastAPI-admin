from datetime import datetime

from fastapi import APIRouter, Depends
from typing import List, Optional

from sqlalchemy.orm import Session
from app import crud
from app.api.utils.db import get_db
from app.api.utils.session import get_current_active_user
from app.schemas.payment import Payment, PaymentCreate, PaymentUpdate
from app.schemas.reponse import PageResponse
from app.models.user import User as DBUser
from app.api.utils.page import pagination


router = APIRouter()


@router.get("/", response_model=PageResponse)
async def get_payments(
    db: Session = Depends(get_db),
    page: int = 0,
    limit: int = 100,
    start_time: Optional[datetime]=None,
    end_time: datetime=datetime.today(),
    current_user: DBUser = Depends(get_current_active_user)
):
    records = crud.payment.get_multi_by_owner(db, start_time=start_time, end_time=end_time, owner_id=current_user.id)
    return pagination(records, page, limit)


@router.post("/", response_model=List[Payment])
def create_payments(
    *,
    db: Session = Depends(get_db),
    payment_list: List[PaymentCreate],
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Create new item.
    """
    payments = crud.payment.create_multi_by_owner(
        db_session=db, obj_in=payment_list, owner_id=current_user.id
    )
    return payments