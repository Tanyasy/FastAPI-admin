import os
from datetime import datetime
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body
from typing import List, Optional

from sqlalchemy.orm import Session
from app import crud
from app.api.utils.db import get_db
from app.api.utils.session import get_current_active_user
from app.schemas.payment import Payment, PaymentCreate, PaymentUpdate
from app.schemas.reponse import PageResponse
from app.models.user import User as DBUser
from app.api.utils.page import pagination
from app.core import config

router = APIRouter()


@router.post("/file/")
async def create_file(
        file: UploadFile = File(...)
):
    file_path = os.path.join(config.UPLOAD_PATH, file.filename)
    if file_path.split(".")[-1] not in config.ACCEPT_FILE_TYPE:
        raise HTTPException(
            status_code=400,
            detail=f"The types of files allowed to upload are {','.join(config.ACCEPT_FILE_TYPE)}.",
        )
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        return {
            "status": 200,
            "fileName": file.filename
        }
    except IOError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Upload file failed, because: {e}.",
        )


@router.put("/import/")
async def import_data(
        db: Session = Depends(get_db),
        file_name: str = Body(..., embed=True),
        current_user: DBUser = Depends(get_current_active_user)
):
    file_path = os.path.join(config.UPLOAD_PATH, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=400,
            detail=f"The file is not exists.",
        )
    data_frame: pd.DataFrame = pd.read_csv(file_path, encoding="GBK")

    data_frame = data_frame.rename(columns=lambda x: x.strip())

    for item in data_frame:
        print(f"=={item}==")
    # 筛选冗余数据
    format_data: pd.DataFrame = data_frame[
        (data_frame["收/支"].apply(lambda x: not str(x).isspace())) & (data_frame["成功退款（元）"] == 0)]

    data: list = []
    for index, row in format_data.iterrows():
        data.append({
            "money": row["金额（元）"],
            "counter_party": row["交易对方"].strip(),
            "payment": row["收/支"].strip(),
            "product_name": row["商品名称"].strip(),
            "trade_sources": row["交易来源地"].strip(),
            # "create_time": datetime.strptime(row["交易创建时间"].strip(),'%Y/%m/%d %H:%M'),
            # "update_time": datetime.strptime(row["最近修改时间"].strip(),'%Y/%m/%d %H:%M'),
            "create_time": row["交易创建时间"].strip().replace(" ", "T").replace("/", "-") + ":00",
            "update_time": row["最近修改时间"].strip().replace(" ", "T").replace("/", "-") + ":00",
        })

    payments = crud.payment.create_multi_by_owner(
        db_session=db, obj_in=data, owner_id=current_user.id
    )
    return {
        "status": 200,
        "total": len(payments)
    }


@router.get("/", response_model=PageResponse)
async def get_payments(
        db: Session = Depends(get_db),
        page: int = 0,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: datetime = datetime.today(),
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


@router.delete("/{id}", response_model=Payment)
def delete_item(
        *,
        db: Session = Depends(get_db),
        id: str,
        current_user: DBUser = Depends(get_current_active_user),
):
    """
    Delete an item.
    """
    item = crud.payment.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.payment.remove(db_session=db, id=id)
    return item
