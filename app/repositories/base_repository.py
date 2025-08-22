# repositories/base_repository.py
import uuid

from sqlalchemy.orm import Session
from typing import Generic, Type, TypeVar

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    # ---- Normal ----
    def get_all(self) -> list[T]:
        return self.db.query(self.model).filter(self.model.is_active.is_(True)).all()

    def get_by_id(self, item_id: int | uuid.UUID) -> T | None:
        return self.db.query(self.model).filter_by(id=item_id).first()

    def get_by_email(self, user_email: str) -> T | None:
        return self.db.query(self.model).filter(self.model.email == user_email).first()


    # ---- Paginated ----
    def get_all_paginated(self, skip: int = 0, limit: int = 10) -> list[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(self.model).count()

    def get(self, item_id: int|uuid.UUID) -> T | None:
        return self.db.query(self.model).filter_by(id=item_id, is_active=True).first()

    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, item_id: int) -> bool:
        obj = self.get(item_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
