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
    # exp属于过期时间，sub是jwt面向的用户，这部分信息一起放在payload里面，pyjwt在decode时如果payload有exp字段会自动进行校验
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
