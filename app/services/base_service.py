# services/base_service.py
import uuid
from typing import Generic, TypeVar, Dict, Any

from fastapi import HTTPException,status

from app.repositories.base_repository import BaseRepository

T = TypeVar("T")

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    # ---- Normal ----
    def get_all(self) -> list[T]:
        return self.repository.get_all()

    def get_total(self) -> int:
        return self.repository.count()

    # ---- Paginated ----
    def get_all_paginated(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        total = self.repository.count()
        items = self.repository.get_all_paginated(skip=skip, limit=limit)
        return {
            "total": total,
            "page": skip,
            "size": limit,
            "items": items,
        }

    def get_by_id(self, item_id: uuid.UUID,user) -> T:  # T is the model type
        obj: T = self.repository.get(item_id)  # explicitly type obj
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with id {item_id} not found"
            )
        if user.id!=obj.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized")

        return obj

    def get_by_email(self, email: str) -> T:  # T is the model type
        obj: T = self.repository.get_by_email(email)  # explicitly type obj
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with email {email} not found"
            )
        return obj

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
