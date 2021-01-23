from fastapi import APIRouter

from .endpoints import users, login, payment, trade_type


api_router = APIRouter()
# prefix:前缀，tags：openapi的信息
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])
api_router.include_router(trade_type.router, prefix="/trade_type", tags=["trade_type"])