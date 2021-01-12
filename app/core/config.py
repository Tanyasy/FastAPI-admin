import os
from app.core.security import AES256Crypto
import base64


# project
PROJECT_NAME="walle board"
API_V1_STR = "/api/v1"

# server
PORT=8080

# security
SECRET_KEY = os.getenv("SECRET_KEY")
FIRST_IV = 'NjtP47eSECuOm3s6'
# 解密对象
aes = AES256Crypto(SECRET_KEY, iv=FIRST_IV)

# db
DATABASE_PASSWORD = "j9IAL+3pyaa77YT92NGFTg=="

DATABASE_URI = (
    "mysql+pymysql://root:%s@localhost:3306/walle"%aes.decrypt(DATABASE_PASSWORD, decode=base64.b64decode)
)
