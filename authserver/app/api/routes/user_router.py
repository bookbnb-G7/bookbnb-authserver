from typing import Optional
from app.services.auth import auth
from fastapi import APIRouter, Header
from app.api.crud.registered_user_dao import RegisteredUserDAO
from app.api.models.registered_user_model import (RegisteredUserSchema,
												  RegisteredUserDB)
router = APIRouter()

@router.get('/id', status_code=200)
async def get_user_uuid(
	api_key: Optional[str] = Header(None),
	x_access_token: Optional[str] = Header(None),	
):
	auth.verify_apy_key(api_key)
	user_data = auth.verify_access_token(x_access_token)
	
	user = RegisteredUserDAO.get_by_email(user_data['email'])
	return user


@router.post('/registered', response_model=RegisteredUserDB, status_code=200)
async def add_registered_user(
	payload: RegisteredUserSchema,
	api_key: Optional[str] = Header(None),
	x_acces_token: Optional[str] = Header(None)
):
	auth.verify_apy_key(api_key)
	auth.verify_access_token(x_access_token)
	
	user = RegisteredUserDAO.add_new_registered_user(payload)
	return user