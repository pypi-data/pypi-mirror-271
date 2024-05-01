from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from systema.management import Settings
from systema.models.auth import Token, User, UserBase

from .utils import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)

router = APIRouter(tags=["auth"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    permanent: bool = False,
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expiration = timedelta(minutes=Settings().access_token_expire_minutes)
    if permanent:
        expiration = None
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=expiration
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
