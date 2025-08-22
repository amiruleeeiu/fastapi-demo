import uuid
from typing import Optional
from pydantic import BaseModel

from app.schemas.contact_info_schema import ContactInfoResponse
from app.schemas.family_info_schema import FamilyInfoResponse


class UserBase(BaseModel):
    id: Optional[uuid.UUID] = None
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class UserCreateRequest(BaseModel):
    email:str
    first_name:str
    last_name:str


class UserUpdateRequest(BaseModel):
    pass

class UserRequest(UserBase):
    pass

class UserResponse(UserBase):
    id: uuid.UUID