import os
import sys
sys.path.append(os.getcwd())
from fastapi import FastAPI
from starlette.requests import Request

from core import config
from app.db.session import Session


app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=config.PORT)