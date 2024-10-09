from typing_extensions import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from riskrate_backend.model.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(token):
    return User(
        name=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    return user
