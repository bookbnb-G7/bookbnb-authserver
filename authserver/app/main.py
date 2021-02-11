from app.api.routes import auth_router, user_router, users_router
from app.db import Base, engine
from app.errors.auth_error import AuthException
from app.errors.bookbnb_error import BookbnbException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

Base.metadata.create_all(engine)

app = FastAPI(title="bookbnb-authserver", description="authserver API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error = {"error": str(exc)}
    return JSONResponse(status_code=400, content=error)


@app.exception_handler(SQLAlchemyError)
async def sql_exception_handler(request, exc):
    error = {"error": str(exc.__dict__['orig'])}
    return JSONResponse(status_code=500, content=error)


app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(users_router.router, prefix="/users", tags=["users"])
