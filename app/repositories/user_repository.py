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

    def create(self,create_user:UserCreateRequest):
        new_user=User(email=create_user.email,
                      first_name=create_user.first_name,
                      last_name=create_user.last_name)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def update(self,user:UserCreateRequest,user_id):
        existing_user=self.get_by_id(user_id)

        # update_fields = existing_user.dict(exclude_unset=True)
        # for key, value in update_fields.items():
        #     setattr(existing_user, key, value)

        existing_user.email=user.dict().get("email")
        existing_user.first_name = user.dict().get("first_name")
        existing_user.last_name = user.dict().get("last_name")

        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user