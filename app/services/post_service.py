from sqlalchemy.orm import Session
from app.repositories.post_repository import PostRepository
from app.services.base_service import BaseService
from app.schemas.post_schema import PostCreate

class PostService(BaseService[PostRepository]):
    def __init__(self, db: Session):
        repo = PostRepository(db)
        super().__init__(repo)

    # --- PostService methods ---
    def get_all_posts(self):
        return self.repo.get_all()

    def create_post(self, post: PostCreate):
        return self.repo.create(post)

    def update_post(self, post_id: int, updated_post: PostCreate):
        return self.repo.update(post_id, updated_post)
