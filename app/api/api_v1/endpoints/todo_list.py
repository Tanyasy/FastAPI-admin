import os
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body, Path, Request
from fastapi.encoders import jsonable_encoder
import json
from typing import List, Optional
from aioredis import Redis
from sqlalchemy.orm import Session
from app import crud
from app.api.utils.db import get_db
from app.api.utils.session import get_current_active_user
from app.schemas.todo_list import TodoList, TodoListCreate, TodoListUpdate
from app.schemas.reponse import PageResponse, Response
from app.models.user import User as DBUser
from app.api.utils.page import pagination
from app.core import config
from app.core.logger import logger

router = APIRouter()


@router.get("/")
async def get_todo_list(
        db: Session = Depends(get_db),
        status: int = None,
        current_user: DBUser = Depends(get_current_active_user),
):
    """
    获取未完成的
    获取已完成的
    获取指定日期的
    :param db:
    :param current_user:
    :return:
    """
    logger.info(f"status is {status}")
    return crud.todo_list.get_multi_by_owner(db, status=status, owner_id=current_user.id)


@router.post("/")
async def create_todo_list(
        request: Request,
        object_in: TodoListCreate,
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user),

):
    object_in.user_id = current_user.id

    result = crud.todo_list.create(db, obj_in=object_in)
    # json_str = jsonable_encoder(result)
    redis = request.app.state.redis  # type: Redis
    # redis.hset()
    await redis.set(f"todo:{result.id}", json.dumps(jsonable_encoder(result)))
    return result


@router.put("/{id}")
async def update_todo_list(
        *,
        id: str = Path(..., min_length=32, max_length=32),
        object_in: TodoListUpdate,
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user),
):
    todo_item = crud.todo_list.get(db, id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Item not found")
    result = crud.todo_list.update(db, db_obj=todo_item, obj_in=object_in)
    if result:
        doing_list = crud.todo_list.get_multi_by_owner(db, status=0, owner_id=current_user.id)
        finished_list = crud.todo_list.get_multi_by_owner(db, status=2, owner_id=current_user.id)
        return {"doingList": doing_list, "finishedList": finished_list}


"""
{
  "create_time": "2021-03-23T21:05:38",
  "id": "c92eefebbb6a416ebb6610e0289d74b3",
  "sort_value": null,
  "priority": 1,
  "user_id": "ad146aecc5a7453a83eaa08482c8ea45",
  "title": "这是标题",
  "update_time": "2021-03-23T21:05:38",
  "is_delete": false,
  "status": 0,
  "project_id": null,
  "parent_id": null,
  "desc": "这是一段描述"
}"""
