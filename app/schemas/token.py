from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    tiktok_name: str


class TokenPayload(BaseModel):
    user_id: str = None