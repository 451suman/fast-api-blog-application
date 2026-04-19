from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class UserSchemaOut(BaseModel):
    name: str
    email: str

    class config:
        from_attributes = True


from typing import List


class Blog(BlogBase):
    class config:
        from_attributes = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog] = []

    class config:
        from_attributes = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    password: str


# ------------------------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
