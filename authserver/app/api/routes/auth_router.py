from typing import Optional
from fastapi import APIRouter, Header
from app.services.auth import auth_service

router = APIRouter()


@router.post('/sign-in', status_code=200)
async def sign_in(
    api_key: Optional[str] = Header(None),
    x_access_token: Optional[str] = Header(None),
):
    auth_service.verify_apy_key(api_key)
    auth_service.verify_access_token(x_access_token)
    return {'message': 'ok'}
