from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core import config


engine = create_engine(config.DATABASE_URI)
# 通过scoped_session函数对原始的Session工厂进行处理，返回出一个ScopedSession工厂，在每个请求来的时候就可以通过这个工厂获得一个 scoped_session 对象
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)