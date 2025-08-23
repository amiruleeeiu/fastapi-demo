import uuid

from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User
from app.schemas.post_schema import PostCreate
from app.repositories.base_repository import BaseRepository
from app.services.base_service import BaseService


class PostRepository(BaseRepository[Post]):
    def __init__(self, db: Session):
        super().__init__(Post, db)
        self.base_service = BaseService(self)

    def get_all(self):
        return self.db.query(Post).all()

    def get_all_by_user(self,user_id:uuid.UUID):
        return self.db.query(Post).filter(Post.user_id==user_id).all()

    def create_post(self, post: PostCreate,user:User):
        print(user)
        new_post = Post(title=post.title, content=post.content,user_id=user.id)
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)
        return new_post

    def update(self, post_id: int, updated_post: PostCreate):
        post = self.base_service.get_by_id(post_id)  # use repository method
        if not post:
            return None
        post.title = updated_post.title
        post.content = updated_post.content
        self.db.commit()
        self.db.refresh(post)
        return post
