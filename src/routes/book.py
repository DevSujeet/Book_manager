from fastapi import APIRouter, Depends
from fastapi.logger import logger
from src.schemas.book import BookCreateSchema, BookResponseSchema
from src.controller.book import create_book_entry, all_book, get_book_by_id
from src.config.configs import _db_settings
from typing import Dict
from src.config.log_config import logger
from src.schemas.pagination.pagination import PageParams, PagedResponseSchema

# from src.schema.book import Book
router = APIRouter(
    prefix="/book",
    tags=["book"]
)

@router.post('')
async def create_book(book:BookCreateSchema) -> BookResponseSchema:
    created_book = create_book_entry(user_id="123", book=book)
    return created_book

@router.post('/all' ,response_model=PagedResponseSchema[BookResponseSchema]) 
async def get_all_books(page_params: PageParams):
    logger.info("Fetching all books")
    all_books = all_book(user_id="123", page_params=page_params)
    return all_books

@router.get('/{book_id}')   
async def get_book(book_id: str) -> Dict[str, str]:
    logger.info(f"Fetching book with ID: {book_id}")
    # Simulate fetching a book by ID logic
    return {"message": f"book with id {book_id}"}

@router.get('/{book_id}/author')
async def get_book_author(book_id: str) -> Dict[str, str]:
    logger.info(f"Fetching author for book with ID: {book_id}")
    # Simulate fetching book author logic
    return {"message": f"author of book with id {book_id}"}
@router.get('/info')
async def about() -> str:
    return "great book"