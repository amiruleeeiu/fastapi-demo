from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.post_schema import PostCreate, PostResponse
from app.services.post_service import PostService
from sqlalchemy.orm import Session
from fastapi import status

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return PostService(db).create_post(post)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    updated = PostService(db).update_post(post_id, post)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return updated

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostService(db).get_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.get("", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return PostService(db).get_all_posts()
