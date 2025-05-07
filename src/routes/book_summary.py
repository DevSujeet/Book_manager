from fastapi import APIRouter, Depends
from fastapi.logger import logger
from typing import Dict
from src.config.log_config import logger
from src.schemas.book_summary import BookSummaryResponse
from src.schemas.pagination.pagination import PageParams, PagedResponseSchema
from src.controller.book_summary import all_book_summary,get_book_summary_by_book_id,get_book_summary_by_id
# from src.schema.book import Book
router = APIRouter(
    prefix="/book_summary",
    tags=["book_summary"]
)

@router.get('/{book_id}')
async def get_book_summary(book_id: str) -> Dict[str, str]:
    logger.info(f"Fetching book summary with ID: {book_id}")
    # Simulate fetching a book summary by ID logic
    book = get_book_summary_by_book_id(user_id="123", id=book_id)
    return book

@router.post('/all' ,response_model=PagedResponseSchema[BookSummaryResponse])
async def get_all_book_summary(page_params: PageParams):
    logger.info("Fetching all book summaries")
    all_books = all_book_summary(user_id="123", page_params=page_params)
    return all_books

@router.get('/summary/{id}')
async def get_book_summary_by_id(id: str) -> Dict[str, str]:
    logger.info(f"Fetching book summary with ID: {id}")
    book = get_book_summary_by_id(user_id="123", id=id)
    return book

@router.get('/user/{user_id}')
async def get_book_summary_by_user_id(user_id: str) -> Dict[str, str]:
    logger.info(f"Fetching book summaries for user ID: {user_id}")
    book = get_book_summary_by_book_id(user_id="123", id=user_id)
    return book