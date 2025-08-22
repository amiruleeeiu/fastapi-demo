

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class ContactInfo(Base):
    __tablename__ = 'contact_info'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    def __repr__(self):
        return f"<ContactInfo(id={self.id}, user_id={self.user_id}, email={self.email}, phone={self.phone})>"