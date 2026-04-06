from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


from typing import List


class Blog(BlogBase):
    class config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog] = []

    class config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True
