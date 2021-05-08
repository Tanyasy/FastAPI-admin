from fastapi import APIRouter, Depends
from app.api.utils.permission import func_user_has_permissions

from .endpoints import users, login, payment, trade_type, role, permission, todo_list, car


api_router = APIRouter()
# prefix:前缀，tags：openapi的信息
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])
api_router.include_router(trade_type.router, prefix="/trade_type", tags=["trade_type"])
api_router.include_router(role.router, tags=["role"], dependencies=[Depends(func_user_has_permissions(["roleCURD"]))])
api_router.include_router(permission.router, tags=["permission"], dependencies=[Depends(func_user_has_permissions(["permissionCURD"]))])
api_router.include_router(todo_list.router, prefix="/todo_list", tags=["todo_list"])
api_router.include_router(car.router, prefix="/car", tags=["car"])