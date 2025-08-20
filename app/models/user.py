

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import contact_info


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact_info_id = Column(Integer, ForeignKey('contact_info.id'), nullable=True)
    family_info_id = Column(Integer, ForeignKey('family_info.id'), nullable=True)

    family_info = relationship("FamilyInfo")
    contact_info = relationship("ContactInfo")
