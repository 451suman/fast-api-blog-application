from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


def success_response(message, status_code=200, data=None):
    return JSONResponse(
        status_code=status_code,
        content={"success": True, "message": message, "data": data},
    )


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None


@app.post("/blog")
def create_blog(request: Blog):
    breakpoint()
    return {
        "success": True,
        "data": {
            "title": request.title,
            "body": request.body,
            "published": request.published,
        },
    }
