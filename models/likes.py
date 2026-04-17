from pydantic import BaseModel


class Likes(BaseModel):
    userId: str
    postId: str