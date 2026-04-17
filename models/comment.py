from pydantic import BaseModel

class Comment(BaseModel):
    userId: str
    postId: str
    text: str
    date: str
    img: str
