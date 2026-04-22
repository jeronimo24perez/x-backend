from pydantic import BaseModel
class Auth_request(BaseModel):
    token: str