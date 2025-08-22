import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.deps import verify_token
from app.core.config import settings
from app.database import get_db
from app.exceptions import NotFoundException
from app.schemas.paginated_response import PaginatedResponse
from app.schemas.user_schema import UserResponse, UserCreateRequest, UserUpdateRequest
from app.services.user_service import UserService
import requests

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), user=Depends(verify_token)):
    """Get all users with their contact and family info"""
    print(f"User info {user}")
    users = UserService(db).get_all()
    return users

@router.get("/pageable",response_model=PaginatedResponse[UserResponse])
def get_paginated_posts(skip:int,limit:int,db: Session = Depends(get_db)):
    return UserService(db).get_all_paginated(skip,limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a user by ID with their contact and family info"""
    user = UserService(db).get_by_id(user_id)
    if not user:
        raise NotFoundException(resource="User")
    return user
#
# @router.get("/simple")
# def get_users_simple(db: Session = Depends(get_db)):
#     """Get all users without joined data"""
#     users = UserService.get_users_simple(db)
#     return users


@router.post("", response_model=UserResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    """Create a new user"""
    return UserService(db).create_post(user)

#
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: uuid.UUID, user: UserCreateRequest, db: Session = Depends(get_db)):

    updated_user = UserService(db).update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

