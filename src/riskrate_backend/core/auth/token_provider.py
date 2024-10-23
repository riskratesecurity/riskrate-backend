from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from riskrate_backend.core.auth.hash_provider import verify_password
from riskrate_backend.model.base import TokenData
from riskrate_backend.model.models import User
from riskrate_backend.core.database import SessionLocal
from sqlalchemy import select

SECRET_KEY = "40281381149b7f7910cd376611d27805af279b53ec7d3b1e7c28fab2fb47c8c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
session = SessionLocal()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    json_dados = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    json_dados.update({"exp": expire})

    jwt_encoded = jwt.encode(json_dados, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encoded

def get_user(username):
    stmt = select(User).where(User.email == username)
    result = session.execute(stmt)
    return result.scalars().first()