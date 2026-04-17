from pydantic import BaseModel


class Follow(BaseModel):
    followerId: str
    followedId: str