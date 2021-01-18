
from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session
from app import crud
from app.api.utils.db import get_db
from app.api.utils.session import get_current_active_user
from app.schemas.payment import Payment, PaymentCreate, PaymentUpdate
from app.models.payment import Payment as DBPayment
from app.models.user import User as DBUser


router = APIRouter()


@router.get("/", response_model=List[Payment])
async def get_payments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_active_user)
):
    return crud.payment.get_multi_by_owner(db, skip=skip, limit=limit, owner_id=current_user.id)


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