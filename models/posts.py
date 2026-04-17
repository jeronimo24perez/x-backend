from pydantic import BaseModel

class Post(BaseModel):
    userId: str
    text: str
    likes: int
    date: str
    img: str
