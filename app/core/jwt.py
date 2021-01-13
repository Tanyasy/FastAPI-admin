from datetime import datetime, timedelta
from copy import copy
import jwt

from app.core import config

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 默认15分钟过期
        expire = datetime.utcnow() + timedelta(minutes=15)
    # todo: 不太懂为啥加sub
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
