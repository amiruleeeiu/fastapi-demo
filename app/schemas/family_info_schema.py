
from typing import Optional
from pydantic import BaseModel


class FamilyInfoBase(BaseModel):
    id: Optional[int] = None
    father_name: str
    mother_name: str

    class Config:
        from_attributes = True

class FamilyInfoRequest(FamilyInfoBase):
    pass

class FamilyInfoResponse(FamilyInfoBase):
    pass