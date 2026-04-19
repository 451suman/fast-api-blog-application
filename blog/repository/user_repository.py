from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog import models
from blog.hashing import Hash
from blog.schemas import ShowUser, UserSchema


def create(request: UserSchema, db: Session):
    existing_user = (
        db.query(models.User).filter(models.User.email == request.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Create new user
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hash(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  # FastAPI will use UserResponseModel and ignore password


def get_user_with_blog(user_id, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user
