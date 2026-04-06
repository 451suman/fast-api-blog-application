from fastapi import FastAPI, Depends, status, HTTPException, Response
from blog.schemas import BlogBase, ShowBlog, ShowUser, UserSchema
from blog import models
from blog.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from typing import List
from blog.routers import blog_router

app = FastAPI()
# models.Base.metadata.drop_all(bind=engine)
# uvicorn blog.main:app --reload --host 0.0.0.0 --port 8000
models.Base.metadata.create_all(engine)


app.include_router(blog_router.router)


from blog.hashing import Hash


@app.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser,
    tags=["user"],
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


@app.get("/user/{id}", response_model=ShowUser, status_code=200, tags=["user"])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user
