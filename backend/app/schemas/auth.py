from pydantic import BaseModel


class VerifyRequest(BaseModel):
    password: str


class VerifyResponse(BaseModel):
    token: str
    expires_in: int
