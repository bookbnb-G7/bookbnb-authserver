from typing import Optional
from fastapi import APIRouter, Header
from app.utils.token_utils import check_token
from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import (RegisteredUserSchema,
												  RegisteredUserDB)

router = APIRouter()

@router.post('/sign-in', status_code=200)
async def sign_in(acces_token: Optional[str] = Header(None)):
	check_token(acces_token)
	return {'message': 'ok'}

@router.post('/registered-user', response_model=RegisteredUserDB, status_code=200)
async def add_registered_user(
	payload: RegisteredUserSchema, acces_token: Optional[str] = Header(None)
):
	check_token(acces_token)
	user = RegisteredUserDAO.add_new_registered_user(payload)
	return user
