from sqlalchemy import Column, DateTime, String, Boolean, func
import uuid
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

class BaseEntity(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    review = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
