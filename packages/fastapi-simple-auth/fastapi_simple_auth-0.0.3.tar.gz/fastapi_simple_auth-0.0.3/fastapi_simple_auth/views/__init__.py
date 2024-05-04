
import json
from typing import Annotated
from pydantic import BaseModel, EmailStr

from fastapi import Request, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..router import auth_router
from ..templates import template_env
from ..settings import settings

from .. import crud, schemas
from ..db import get_db
from ..exceptions import SimpleAuthVerificationAlreadySent
from ..cron import cron

from . import login, profile, settingsjs, signup, verify, recover

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


#class UNUSED_UserInDB(User):
#    hashed_password: str





@auth_router.post("/token")
async def UNUSED_login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    
    user = crud.get_auth_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uuid}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


