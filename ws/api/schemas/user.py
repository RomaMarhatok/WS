from pydantic import BaseModel


class POSTUserSchema(BaseModel):
    username: str
    password: str
