from fastapi import FastAPI, Depends, status, HTTPException, Response
from blog.schemas import BlogBase, ShowBlog, ShowUser, UserSchema
from blog import models
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from typing import List

app = FastAPI()
# models.Base.metadata.drop_all(bind=engine)
# uvicorn blog.main:app --reload --host 0.0.0.0 --port 8000
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/blog", status_code=status.HTTP_201_CREATED, description="hello", tags=["blogs"]
)
def create(request: BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get(
    "/blog",
    response_model=List[ShowBlog],
    status_code=status.HTTP_200_OK,
    tags=["blogs"],
)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", response_model=ShowBlog, tags=["blogs"])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        # return {"success": False, "message": "Blog not found"}
        raise HTTPException(status_code=404, detail="Blog not Found.")

    response.status_code = status.HTTP_200_OK
    return blog
    # return {
    #     "success": True,
    #     "data": {"id": blog.id, "title": blog.title, "body": blog.body},
    # }


@app.delete("/blog/{id}", tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    db.delete(blog)  # ✅ delete the instance
    db.commit()  # ✅ commit transaction


@app.put("/blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
def update(id, request: BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")

    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog


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
