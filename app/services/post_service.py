import uuid
from fastapi import HTTPException,status
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

    def update_post(self, post_id: uuid.UUID, updated_post: PostCreate,user:User):
        post = self.repo.get_by_id(post_id)  # use repository method

        if post.user_id!=user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized"
            )

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found"
            )

        return self.repo.update(post_id,post,updated_post)
