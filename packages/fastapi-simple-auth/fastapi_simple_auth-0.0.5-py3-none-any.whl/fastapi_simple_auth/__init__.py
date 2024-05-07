from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import logging

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


from jose import JWTError, jwt

from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session

from . import schemas, crud, views
from .router import auth_router
from .settings import settings
from .verification import send_verification_signup
from .templates import template_env
from .startup import startup
from .models import User
from .pub import logged_in_user
from . import views

__version__ = '0.0.5'

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# suppress AttributeError: module 'bcrypt' has no attribute '__about__'
logging.getLogger('passlib').setLevel(logging.ERROR)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# startup(auth_router)


def package_path():
    return os.path.dirname(__file__) # .replace("simpleauth/__init__.py", "")


startup()

# api_auth.mount("/static", StaticFiles(directory="static"), name="static")


#def get_user(db, username: str):
#    if username in db:
#        user_dict = db[username]
#        return UserInDB(**user_dict)



class SimpleAuth():
    def __init__(self, app: FastAPI):
        self.app = app
        self.register()

    def register(self):
        self.app.add_middleware(SessionMiddleware, secret_key='ChangeMe', max_age=None)
        self.app.include_router(auth_router, prefix="/auth")
        self.app.mount("/auth/static", 
                       StaticFiles(packages=[settings.template_theme]), 
                       name="simpleauth-static")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




async def get_current_user_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def __main__():
    print("mmm")