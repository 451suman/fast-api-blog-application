from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from sqlalchemy.orm import Session

from blog import models
from blog.database import get_db
from blog.schemas import BlogBase, ShowBlog


router = APIRouter()


@router.get(
    "/blog",
    response_model=List[ShowBlog],
    status_code=status.HTTP_200_OK,
    tags=["blogs"],
)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post(
    "/blog", status_code=status.HTTP_201_CREATED, description="hello", tags=["blogs"]
)
def create(request: BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/blog/{id}", response_model=ShowBlog, tags=["blogs"])
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


@router.delete("/blog/{id}", tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    db.delete(blog)  # ✅ delete the instance
    db.commit()  # ✅ commit transaction


@router.put("/blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
def update(id, request: BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")

    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog
