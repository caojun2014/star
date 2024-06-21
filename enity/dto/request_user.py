from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    userAccount: str
    userPassword: str
    checkPassword: str