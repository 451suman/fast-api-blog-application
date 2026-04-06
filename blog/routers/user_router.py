from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from blog import models
from blog.database import get_db
from blog.hashing import Hash
from blog.schemas import ShowUser, UserSchema


router = APIRouter(prefix="/api/user", tags=["user"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser,
)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    # Check if a user with the email already exists
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


@router.get("/{id}", response_model=ShowUser, status_code=200)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user
