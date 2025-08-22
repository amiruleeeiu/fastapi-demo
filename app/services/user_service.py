import uuid
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateRequest
from app.services.base_service import BaseService
from app.models.user import User
from app.services.keycloak_service import KeycloakService


class UserService(BaseService[UserRepository]):
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        super().__init__(self.repo)

    def create_post(self, user: UserCreateRequest):
        existing_user = self.repo.get_by_email(user.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user.email} has already exist"
            )

        user_data = {
            "username": user.email,
            "email": user.email,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "enabled": True,
            "emailVerified": True,
            "credentials": [{
                "type": "password",
                "value": settings.DEFAULT_PASSWORD,
                "temporary": True  # Forces password change on first login
            }]
        }

        # Create in Keycloak first
        keycloak_service = KeycloakService()
        keycloak_id = keycloak_service.create_user(user_data=user_data)

        return self.repo.create_user(user,keycloak_id)

    def update_user(self, user_id: uuid.UUID, user: UserCreateRequest) -> User:
        existing_user = self.repo.get_by_id(user_id)  # ✅ Correct type hint

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with id {user_id} not found"
            )

        print(existing_user)

        for key, value in user.dict(exclude_unset=True).items():
            setattr(existing_user, key, value)

        updated_user: User = self.repo.update(existing_user)  # returns User
        return updated_user


