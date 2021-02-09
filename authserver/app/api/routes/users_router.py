from typing import Optional

from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import (RegisteredUserDB,
                                                  RegisteredUserSchema)
from app.db import get_db
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/{uuid}", status_code=200)
async def get_user(
    uuid: int,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_api_key(api_key)
    user = RegisteredUserDAO.get_user(uuid)
    return user


@router.post("/users/{uuid}/unblock", status_code=200)
async def block_user(
    uuid: int,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_api_key(api_key)
    blocked_user = RegisteredUserDAO.block_user(db, uuid)
    return blocked_user

@router.post("/users/{uuid}/unblock", status_code=200)
async def unblock_user(
    uuid: int,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_api_key(api_key)
    unblocked_user = RegisteredUserDAO.unblock_user(db, uuid)
    return unblocked_user
