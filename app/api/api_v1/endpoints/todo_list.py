import os
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body
from typing import List, Optional

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
    current_user: DBUser = Depends(get_current_active_user),
):
    return crud.todo_list.get_multi(db)