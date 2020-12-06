from fastapi import FastAPI
from app.db import Base, engine
from app.config import get_settings
from app.config import firebase_authenticate
from starlette.exceptions import HTTPException
from app.errors.auth_errors import AuthException

from app.api.routes import auth_router 

Base.metadata.create_all(engine)

app = FastAPI(
    title="bookbnb-authserver", description="Especificacion sobre la API del authserver"
)

@app.get("/")
async def pong():
    return {"message": "authserver"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)

@app.exception_handler(AuthException)
async def auth_exception_handler(request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)

app.include_router(
	auth_router.router, prefix="/auth", tags=["auth"]
)


