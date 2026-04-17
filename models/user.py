from typing import Annotated

from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str
    bio: str
    location: str
    website: str
    follows: int
    followers: int
    date: str
