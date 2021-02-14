from typing import Optional

from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import (RegisteredUserDB,
                                                  RegisteredUserSchema)
from app.db import get_db
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

router = APIRouter()


# Expects an x-access-token of a registered user and returns
# a RegisteredUserDB json ({uuid, email, blocked, created_at, updated_at})
@router.get("/id", status_code=200)
async def get_user_uuid(
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None),
):
    auth_service.verify_api_key(api_key)
    user_data = auth_service.verify_access_token(x_access_token)
    user = RegisteredUserDAO.get_by_email(db, user_data["email"])
    return user


# Expects an x-access-token and the email of a user that exists in firebase and
# to create it in the authserver database and generate a new uuid
# It returns RegisteredUserDB json ({uuid, email, blocked, created_at, updated_at})
@router.post("/registered", response_model=RegisteredUserDB, status_code=201)
async def add_registered_user(
    payload: RegisteredUserSchema,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None),
):
    auth_service.verify_api_key(api_key)
    auth_service.verify_access_token(x_access_token)
    user = RegisteredUserDAO.add_new_registered_user(db, payload, False)
    return user


# Expects an x-access-token of a user that exists in firebase and
# deletes it from the authserver database
# It returns RegisteredUserDB json ({uuid, email, blocked, created_at, updated_at})
@router.delete("/registered/{uuid}", response_model=RegisteredUserDB, status_code=200)
async def delete_registered_user(
    uuid: int,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None),
):
    auth_service.verify_api_key(api_key)
    auth_service.verify_access_token(x_access_token)
    user = RegisteredUserDAO.delete_by_uuid(db, uuid)
    return user
