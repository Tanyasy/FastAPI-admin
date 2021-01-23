from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from app import crud
from app.api.utils.db import get_db
from app.schemas.trade_type import TradeType, TradeTypeCreate, TradeTypeUpdate


router = APIRouter()


@router.get("/", response_model=List[TradeType])
async def get_payments(
        db: Session = Depends(get_db),
):
    return crud.trade_type.get_multi(db)


@router.post("/", response_model=List[TradeType])
def create_payments(
        *,
        db: Session = Depends(get_db),
        data_list: List[TradeTypeCreate]
):
    """
    Create new item.
    """
    return crud.trade_type.create_multi(
        db_session=db, obj_in=data_list
    )


@router.delete("/{id}", response_model=TradeType)
def delete_item(
        *,
        db: Session = Depends(get_db),
        id: str
):
    """
    Delete an item.
    """
    item = crud.trade_type.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.trade_type.remove(db_session=db, id=id)
