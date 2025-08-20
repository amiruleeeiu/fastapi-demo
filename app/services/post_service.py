
from sqlalchemy.orm import Session
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostCreate

class PostService:
    def __init__(self,db:Session):
        self.repo=PostRepository(db)

    def create_post(self,post:PostCreate):
        return self.repo.create(post)

    def get_post(self,post_id):
        return self.repo.get_by_id(post_id)

    def update_post(self,post_id:int,updated_post:PostCreate):

        post=self.repo.get_by_id(post_id)
        if not post:
            return None
        post.title=updated_post.title
        post.content=updated_post.content

        return self.repo.update(post)

    def get_all_posts(self):
        return self.repo.get_all()
