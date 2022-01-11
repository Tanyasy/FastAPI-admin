import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import aioredis
import pymysql


from app.core import config
from app.db.session import Session, engine
from app.api.api_v1 import api_router
from app.db.base_class import Base
from app import scheduler

Base.metadata.create_all(bind=engine)
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")
app.include_router(api_router, prefix=config.API_V1_STR)


async def get_redis_pool(redis_url) -> aioredis.Redis:
    pool = aioredis.ConnectionPool.from_url(redis_url, max_connections=10)
    redis = aioredis.Redis(connection_pool=pool)
    # pool = aioredis.ConnectionPool.from_url(config.REDIS_URI, max_connection=10)
    # redis = aioredis.Redis(connection_pool=pool)
    return redis


# 信任域
origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://192.168.31.181:8081",
    "http://192.168.31.194"
]

# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    封装参数校验失败的响应信息
    :param request:
    :param exc:
    :return:
    """
    message = ""
    for items in exc.errors():
        message += items.get("type") + ": " + items.get("msg") + "\n"
    return JSONResponse(
        content={
            "status": status.HTTP_400_BAD_REQUEST,
            "message": message
        },
        status_code=status.HTTP_400_BAD_REQUEST
    )
    pass


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.on_event('startup')
async def startup_event():
    """
    启动时连接redis,并开启定时任务
    :return:
    """
    app.state.redis = await get_redis_pool(config.REDIS_URI)
    app.state.scheduler = scheduler.init_scheduler()


@app.on_event('shutdown')
async def shutdown_event():
    """
    关闭时关闭redis连接
    :return:
    """
    app.state.redis.close()
    await app.state.redis.wait_closed()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
