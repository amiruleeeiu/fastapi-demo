

from sqlalchemy import Column, Integer, String
from app.database import Base


class FamilyInfo(Base):
    __tablename__ = 'family_info'

    id = Column(Integer, primary_key=True, index=True)
    father_name = Column(String, index=True)
    mother_name = Column(String, nullable=False)

    