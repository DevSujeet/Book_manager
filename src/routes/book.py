from fastapi import APIRouter, Depends
from fastapi.logger import logger
from src.schemas.book import BookCreateSchema, BookResponseSchema
from src.controller.book import create_book_entry
from src.config.configs import _db_settings
from typing import Dict
from src.config.log_config import logger

# from src.schema.book import Book
router = APIRouter(
    prefix="/book",
    tags=["book"]
)

@router.post('')
async def create_book(book:BookCreateSchema) -> BookResponseSchema:
    logger.info("Fetching database settings")
    # Simulate book creation logic
    created_book = create_book_entry(user_id="123", book=book)
    return created_book

@router.get('/info')
async def about() -> str:
    return "great book"