from typing import Optional

from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import (RegisteredUserDB,
                                                  RegisteredUserSchema,
                                                  RegisteredUserList)
from app.db import get_db
from app.services.auth import auth_service
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

router = APIRouter()


# Expects an x-access-token and the email of a user that exists in firebase and
# to create it in the authserver database and generate a new uuid
# It returns RegisteredUserDB json ({uuid, email, blocked, created_at, updated_at})
@router.post("", response_model=RegisteredUserDB, status_code=201)
async def add_registered_admin(
    payload: RegisteredUserSchema,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None),
):
    # Check API-KEY
    auth_service.verify_api_key(api_key)

    # Check that x-access-token is from a registered admin
    user_data = auth_service.verify_access_token(x_access_token)
    RegisteredUserDAO.get_admin_by_email(db, user_data["email"])

    # Create the new admin
    user = RegisteredUserDAO.add_new_registered_user(db, payload, True)
    return user


# It returns a list of all the users that have "is_admin" == True in the DB
@router.get("", response_model=RegisteredUserList, status_code=200)
async def get_all_admin_users(
    db: Session = Depends(get_db),
    api_key: Optional[str] = Header(None)
):
    auth_service.verify_api_key(api_key)
    users = RegisteredUserDAO.get_all_admins(db)
    return {"amount": len(users), "users": users}


# Returns a RegisteredUserDB if the x-access-token is valid an
# corresponds to a user logged in firebase that is admin, otherwise
# it returns 404 {"message": "User not found"}
@router.get("/sign-in", response_model=RegisteredUserDB, status_code=200)
async def get_admin(
    db: Session = Depends(get_db),
    x_access_token: Optional[str] = Header(None),
):
    user_data = auth_service.verify_access_token(x_access_token)
    user = RegisteredUserDAO.get_admin_by_email(db, user_data["email"])
    return user
