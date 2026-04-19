from urllib import response
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog import models, schemas


def get_all(db: Session):
    return db.query(models.Blog).all()


def create(request, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_blog(id: int, db: Session):
    print("Fetching blog:", id)
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        print("Blog not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    return blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    db.delete(blog)
    db.commit()
    return


def update(id: int, db: Session, request: schemas.Blog):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")

    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog
