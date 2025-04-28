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
    prefix="/book_summary",
    tags=["book_summary"]
)

@router.get('/{book_id}')
async def get_book_summary(book_id: str) -> Dict[str, str]:
    logger.info(f"Fetching book summary with ID: {book_id}")
    # Simulate fetching a book summary by ID logic
    return {"message": f"Book summary with id {book_id}"}