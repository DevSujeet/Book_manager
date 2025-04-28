from fastapi import APIRouter, Depends
from fastapi.logger import logger
from src.schemas.user import UserCreate, UserResponse
from src.controller.user import create_user_entry, all_users, get_user_by_id, delete_user_by_id
from src.config.configs import _db_settings
from typing import Dict
from src.config.log_config import logger
from src.schemas.pagination.pagination import PageParams, PagedResponseSchema

# from src.schema.book import Book
router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post('')
async def create_user(user: UserCreate) -> UserResponse:
    created_user = create_user_entry(user_id="123", user=user)
    return created_user

@router.post('/all')
async def get_all_users(page_params: PageParams, response_model=PagedResponseSchema[UserResponse]):
    logger.info("Fetching all users")
    all_users = all_users(user_id="123", page_params=page_params)
    return all_users

@router.get('/{user_id}')
async def get_user(user_id: str) -> Dict[str, str]:
    logger.info(f"Fetching user with ID: {user_id}")
    # Simulate fetching a user by ID logic
    return {"message": f"user with id {user_id}"} 

@router.delete('/{user_id}')
async def delete_user(user_id: str) -> Dict[str, str]:
    logger.info(f"Deleting user with ID: {user_id}")
    # Simulate deleting a user by ID logic
    return {"message": f"user with id {user_id} deleted"}