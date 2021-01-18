from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.core import config
from app.models.user import User as DBUser
from app.schemas.user import User, UserCreate
from app.schemas.reponse import Response
from app import crud


router = APIRouter()



# 通过response_model来设置响应模型，可以将对象转化成json数据返回
@router.get("/", response_model=Response)
async def get_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    """
    获取用户列表
    :param db: 数据库session
    :param skip: 偏移
    :param limit: 数据限制
    :return: 用户列表
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)

    return {
        "status": status.HTTP_200_OK,
        "total": len(users),
        "data": users,
        "msg": "ok"
    }

# 第一个参数为*，则后面参数都为位置参数，不管有没有默认值
@router.post("/", response_model=User)
async def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate
):
    """
    创建用户
    :param db: 数据库session
    :param user_in: 输入参数
    :return:
    """
    user = crud.user.get_by_name(db, user_name=user_in.name)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
