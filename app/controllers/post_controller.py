from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.repositories.base_repository import BaseRepository
from app.schemas.paginated_response import PaginatedResponse
from app.schemas.post_schema import PostCreate, PostResponse
from app.services.base_service import BaseService
from app.services.post_service import PostService
from sqlalchemy.orm import Session
from fastapi import status

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return PostService(db).create_post(post)

@router.get("/pageable",response_model=PaginatedResponse[PostResponse])
def get_paginated_posts(skip:int,limit:int,db: Session = Depends(get_db)):
    return PostService(db).get_all_paginated(skip,limit)

@router.get("/number-of-post",response_model=int)
def get_number_of_post(db: Session = Depends(get_db)):
    return PostService(db).get_total()

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    updated = PostService(db).update_post(post_id, post)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return updated

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):

    return PostService(db).get_by_id(post_id)

@router.get("", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return PostService(db).get_all_posts()

