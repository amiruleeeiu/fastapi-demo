import uuid
from calendar import error

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.schemas.user_schema import UserCreateRequest
from app.services.base_service import BaseService


class UserRepository(BaseRepository[User]):
    def __init__(self,db:Session):
        super().__init__(User,db)
        self.base_service=BaseService(self)

    def create_user(self,create_user:UserCreateRequest,keycloak_id:str):
        new_user=User(email=create_user.email,
                      first_name=create_user.first_name,
                      last_name=create_user.last_name,
                      keycloak_id=keycloak_id)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user