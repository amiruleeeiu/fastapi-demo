import uuid

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateRequest
from app.services.base_service import BaseService

class UserService(BaseService[UserRepository]):
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        super().__init__(self.repo)

    def create_post(self, user: UserCreateRequest):
        return self.repo.create(user)

    def update_user(self, user: UserCreateRequest,user_id:uuid.UUID):
        return self.repo.update(user,user_id)

