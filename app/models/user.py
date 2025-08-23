from typing import Optional

from sqlalchemy import String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_entity import BaseEntity

class User(BaseEntity):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    keycloak_id: Mapped[str | None] = mapped_column(String, nullable=False)
