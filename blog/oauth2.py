from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from blog.token import verify_token
from blog.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)
