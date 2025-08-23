import uuid
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_entity import BaseEntity

class Post(BaseEntity):
    __tablename__ = "posts"

    title : Mapped[str] = mapped_column(String,nullable=False)
    content:Mapped[str] = mapped_column(Text)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    # relationship back to user
    user: Mapped["User"] = relationship()