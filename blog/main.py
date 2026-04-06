from fastapi import FastAPI, Depends, status, HTTPException, Response
from blog.schemas import BlogBase, ShowBlog, ShowUser, UserSchema
from blog import models
from blog.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from typing import List
from blog.routers import blog_router, user_router

app = FastAPI()
# models.Base.metadata.drop_all(bind=engine)
# uvicorn blog.main:app --reload --host 0.0.0.0 --port 8000
models.Base.metadata.create_all(engine)


app.include_router(blog_router.router)
app.include_router(user_router.router)
