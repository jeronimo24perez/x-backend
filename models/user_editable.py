from typing import Annotated

from pydantic import BaseModel

class User_editable(BaseModel):
    username: str
    bio: str
    location: str
    website: str
