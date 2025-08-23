import uuid

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.post_repository import PostRepository
from app.services.base_service import BaseService
from app.schemas.post_schema import PostCreate

class PostService(BaseService[PostRepository]):
    def __init__(self, db: Session):
        self.repo = PostRepository(db)
        super().__init__(self.repo)

    # --- PostService methods ---
    def get_all_posts(self,user_id:uuid.UUID):
        return self.repo.get_all_by_user(user_id)

    def create_post(self, post: PostCreate,user:User):
        print(f"user info {user}")
        return self.repo.create_post(post,user)

    def update_post(self, post_id: uuid.UUID, updated_post: PostCreate):
        return self.repo.update(post_id, updated_post)
