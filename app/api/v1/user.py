from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserLogin
from app.schemas.token import Token
from app.services.user_service import UserService
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=User)
async def create_user(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await UserService.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.authenticate_user(
        db,
        UserLogin(email=form_data.username, password=form_data.password)
    )
    return UserService.create_login_token(user)

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 인증된 사용자만 접근 가능
):
    users = await UserService.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 인증된 사용자만 접근 가능
):
    return await UserService.get_user(db, user_id=user_id)