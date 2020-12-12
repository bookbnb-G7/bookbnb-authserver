from fastapi import FastAPI
from app.db import Base, engine
from app.api.routes import auth_router
from app.api.routes import user_router
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from app.errors.auth_error import AuthException
from app.errors.bookbnb_error import BookbnbException

Base.metadata.create_all(engine)

app = FastAPI(
    title="bookbnb-authserver", description="authserver API"
)


@app.get("/")
async def pong():
    return {"message": "authserver"}


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(AuthException)
async def auth_exception_handler(_request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(BookbnbException)
async def bookbnb_exception_handler(_request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)


app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(user_router.router, prefix="/user", tags=["user"])
