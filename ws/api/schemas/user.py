from pydantic import BaseModel


class POSTUserRequest(BaseModel):
    username: str
    password: str
