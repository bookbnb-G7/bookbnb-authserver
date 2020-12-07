from typing import Optional
from app.services.auth import auth
from fastapi import APIRouter, Header
from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import (RegisteredUserSchema,
												  RegisteredUserDB)

router = APIRouter()

@router.post('/sign-in', status_code=200)
async def sign_in(x_access_token: Optional[str] = Header(None)):
	auth.verify_access_token(x_access_token)
	return {'message': 'ok'}