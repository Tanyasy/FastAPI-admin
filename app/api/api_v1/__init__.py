from fastapi import APIRouter

from .endpoints import users, login


api_router = APIRouter()
# prefix:前缀，tags：openapi的信息
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])