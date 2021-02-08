from pydantic import BaseModel


class RegisteredUserSchema(BaseModel):
    email: str


class RegisteredUserDB(RegisteredUserSchema):
    uuid: int
    blocked: bool
