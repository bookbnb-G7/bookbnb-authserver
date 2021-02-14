from pydantic import BaseModel
from typing import List


class RegisteredUserSchema(BaseModel):
    email: str


class RegisteredUserDB(RegisteredUserSchema):
    uuid: int
    blocked: bool


class RegisteredUserList(BaseModel):
    amount: int
    users: List[RegisteredUserDB]
