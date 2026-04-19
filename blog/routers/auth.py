from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from blog.database import get_db
from blog.hashing import Hash
from blog.models import User
from blog.schemas import LoginSchema, Token
from blog.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(request: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password",
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
