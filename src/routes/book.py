from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, File, Form
from fastapi.logger import logger
from src.schemas.book import BookCreateSchema, BookResponseSchema
from src.controller.book import create_book_entry, all_book,delete_book_by_id, get_book_by_id, process_pdf_summary
from src.config.configs import _db_settings
from typing import Dict
from src.config.log_config import logger
from src.schemas.pagination.pagination import PageParams, PagedResponseSchema

# from src.schema.book import Book
router = APIRouter(
    prefix="/book",
    tags=["book"]
)

@router.post("")
async def create_book(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    publisher: str = Form(...),
    publication_year: int = Form(...),
    genre: str = Form(None),
    language: str = Form(...),
    pages: int = Form(...),
    summary: str = Form(None),
    file: UploadFile = File(None)
) -> BookResponseSchema:

    book = BookCreateSchema(
        title=title,
        author=author,
        isbn=isbn,
        publisher=publisher,
        publication_year=publication_year,
        genre=genre or "pending",
        language=language,
        pages=pages,
        summary=summary or "Summary generation pending..."
    )

    created_book = create_book_entry(user_id="123", book=book)

    # If file uploaded, start background task
    if file:
        # background_tasks.add_task(process_pdf_summary, created_book.get("book_id"), file)
        file_bytes = await file.read()  # Read file *now*
        background_tasks.add_task(
            process_pdf_summary, created_book.get("book_id"), file_bytes
        )

    return created_book


@router.post('/all' ,response_model=PagedResponseSchema[BookResponseSchema]) 
async def get_all_books(page_params: PageParams):
    logger.info("Fetching all books")
    all_books = all_book(user_id="123", page_params=page_params)
    return all_books

@router.get('/{book_id}')   
async def get_book(book_id: str) -> Dict[str, str]:
    logger.info(f"Fetching book with ID: {book_id}")
    book = get_book_by_id(user_id="123", id=book_id)
    return book

@router.delete('/{book_id}')
async def delete_book(book_id: str) -> Dict[str, str]:
    logger.info(f"Deleting book with ID: {book_id}")
    deleted_book = delete_book_by_id(user_id="123", book_id=book_id)
    return deleted_book