from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from sqlalchemy.orm import Session
from blog.schemas import UserSchema
from blog import models
from blog.database import get_db
from blog.oauth2 import get_current_user
from blog.schemas import BlogBase, ShowBlog
from blog.repository import blog as blog_repository

router = APIRouter(prefix="/api/blogs", tags=["blogs"])


@router.get(
    "",
    # response_model=List[ShowBlog],
    status_code=status.HTTP_200_OK,
)
def all(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return blog_repository.get_all(db)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="hello",
)
def create(request: BlogBase, db: Session = Depends(get_db)):
    # new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    # return new_blog
    return blog_repository.create(request=request, db=db)


@router.get("/{id}")
def show(id: int, response: Response, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"success": False, "message": "Blog not found"}
    #     raise HTTPException(status_code=404, detail="Blog not Found.")

    # response.status_code = status.HTTP_200_OK
    # return blog
    return blog_repository.get_blog(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
    #     )

    # db.delete(blog)  # delete the instance
    # db.commit()  # commit transaction
    blog_repository.destroy(id=id, db=db)
    return None


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update(id, request: BlogBase, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    # if not blog:
    #     raise HTTPException(status_code=404, detail="blog not found")

    # blog.title = request.title
    # blog.body = request.body
    # db.commit()
    # db.refresh(blog)
    # return blog
    return blog_repository.update(id=id, db=db, request=request)
