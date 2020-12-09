from typing import Optional

from app.services.auth import auth_service
from fastapi import APIRouter, Header

router = APIRouter()


@router.post("/sign-in", status_code=200)
async def sign_in(x_access_token: Optional[str] = Header(None)):
    auth_service.verify_access_token(x_access_token)
    return {"message": "ok"}
