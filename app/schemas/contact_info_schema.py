

from typing import Optional
from pydantic import BaseModel


class ContactInfoBase(BaseModel):
    id: Optional[int] = None
    email: str
    phone: str
    
    class Config:
        from_attributes = True

class ContactInfoRequest(ContactInfoBase):
    pass

class ContactInfoResponse(ContactInfoBase):
    pass