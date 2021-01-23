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

# jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 60 minutes * 24 hours * 8 days = 8 days

# upload file
BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
UPLOAD_PATH = os.path.join(BASE_DIR, "download")
ACCEPT_FILE_TYPE = ["xls", "csv"]
