from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
