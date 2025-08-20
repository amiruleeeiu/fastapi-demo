

from typing import Optional
from pydantic import BaseModel

from app.schemas.contact_info_schema import ContactInfoResponse
from app.schemas.family_info_schema import FamilyInfoResponse


class UserBase(BaseModel):
    id: Optional[int] = None
    name: str
    contact_info_id: Optional[int] = None
    family_info_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserCreateRequest(BaseModel):
    name: str
    family_info: Optional[dict] = None
    contact_info: Optional[dict] = None

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    family_info: Optional[dict] = None
    contact_info: Optional[dict] = None

class UserRequest(UserBase):
    pass

class UserResponse(BaseModel):
    id:int
    name: str
    contact_info: Optional[ContactInfoResponse] = None
    family_info: Optional[FamilyInfoResponse] = None