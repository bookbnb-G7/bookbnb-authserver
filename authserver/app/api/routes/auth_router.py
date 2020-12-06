from typing import Optional
from fastapi import APIRouter, Header
from app.utils.token_utils import check_token

router = APIRouter()

@router.post('/sign-in', status_code=200)
async def sign_in(acces_token: Optional[str] = Header(None)):
	check_token(acces_token)
	return {'message': 'ok'}