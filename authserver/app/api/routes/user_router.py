from app.db import get_db
from typing import Optional
from sqlalchemy.orm import Session
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import RegisteredUserDB, RegisteredUserSchema

router = APIRouter()


@router.get("/id", status_code=200)
async def get_user_uuid(
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None),
):
    auth_service.verify_apy_key(api_key)
    user_data = auth_service.verify_access_token(x_access_token)
    user = RegisteredUserDAO.get_by_email(db, user_data["email"])
    return user


@router.post("/registered", response_model=RegisteredUserDB, status_code=200)
async def add_registered_user(
    payload: RegisteredUserSchema,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None)
):
    auth_service.verify_apy_key(api_key)
    auth_service.verify_access_token(x_access_token)
    user = RegisteredUserDAO.add_new_registered_user(db, payload)
    return user
