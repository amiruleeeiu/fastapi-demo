import uuid

from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateRequest
from app.services.base_service import BaseService
from app.models.user import User

class UserService(BaseService[UserRepository]):
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        super().__init__(self.repo)

    def create_post(self, user: UserCreateRequest):
        return self.repo.create(user)

    def update_user(self, user_id: uuid.UUID, user: UserCreateRequest) -> User:
        existing_user = self.repo.get_by_id(user_id)  # ✅ Correct type hint

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with id {user_id} not found"
            )


        print(existing_user)
        update_fields = user.dict()

        existing_user.email=user.dict().get("email")
        existing_user.first_name = user.dict().get("first_name")
        existing_user.last_name = user.dict().get("last_name")

        updated_user: User = self.repo.update(existing_user)  # returns User
        return updated_user


