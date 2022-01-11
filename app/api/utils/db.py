from starlette.requests import Request


def get_db(request: Request):
    return request.state.db


def get_redis(request: Request):
    return request.app.state.redis


def get_scheduler(request: Request):
    return request.app.state.scheduler
