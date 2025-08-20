from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.exceptions import NotFoundException
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse, UserCreateRequest, UserUpdateRequest


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Get all users with their contact and family info"""
    users = UserService.get_all_users(db)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID with their contact and family info"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException(resource="User")
    return user

@router.get("/simple")
def get_users_simple(db: Session = Depends(get_db)):
    """Get all users without joined data"""
    users = UserService.get_users_simple(db)
    return users


@router.post("", response_model=UserResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    """Create a new user"""
    user_dict = user.dict()
    created_user = UserService.create_user(user_dict, db)
    return created_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdateRequest, db: Session = Depends(get_db)):
    """Update an existing user"""
    user_dict = user.dict(exclude_unset=True)
    updated_user = UserService.update_user(user_id, user_dict, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

