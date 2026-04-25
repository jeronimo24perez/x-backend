from pydantic import BaseModel

class Comment(BaseModel):
    userId: str
    postId: str
    autor: str
    email: str
    text: str
    date: str
    img: str
