
from turtle import title
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.user import User
from app.schemas.post_schema import PostCreate
from app.schemas.user_schema import UserCreateRequest

class PostRepository():
    def __init__(self,db:Session):
        self.db=db

    def get_all(self):
        return self.db.query(Post).all()
    
    def get_by_id(self,post_id:int):
        return self.db.query(Post).filter_by(id=post_id).first()

    def create(self,post:PostCreate):
        new_post=Post(title=post.title,content=post.content)

        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)
        return new_post
    
    def update(self,updated_post:PostCreate):

        self.db.commit()
        self.db.refresh(updated_post)
        return updated_post