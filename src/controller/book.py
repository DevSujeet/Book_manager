
from fastapi import HTTPException, UploadFile
from src.db import get_session
from src.schemas.book import BookCreateSchema
from src.crud.book import BookCRUD
from src.schemas.pagination.pagination import PageParams
from src.utilities.pdf_reader import extract_text_from_pdf
from src.services.deepseek_service import generate_summary_and_genre
import tempfile
import os
import json

def all_book(user_id:str, page_params:PageParams):
    with get_session() as session:
        book = BookCRUD(db_session=session).all_book(page_params=page_params)
        return book

def get_book_by_id(user_id:str, id:str):
     with get_session() as session:
        book = BookCRUD(db_session=session).get_book_by_id(id=id)

        return book

def create_book_entry(user_id: str, book:BookCreateSchema):
    with get_session() as session:
        book_obj = BookCRUD(db_session=session).create_book_entry(book=book)
        if not book_obj:
            raise HTTPException(status_code=400, detail="Book creation failed")
        return book_obj
    

def delete_book_by_id(user_id:str, book_id:str):
    with get_session() as session:
        book = BookCRUD(db_session=session).delete_book_by_id(id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    

async def process_pdf_summary(book_id: str, file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        text = extract_text_from_pdf(temp_file_path)
        ai_result = await generate_summary_and_genre(text)
        ai_response = json.loads(ai_result["response"])

        summary = ai_response.get("summary")
        genre = ai_response.get("genre")

        # Update the book record
        with get_session() as session:
            BookCRUD(db_session=session).update_book_summary_genre(book_id, summary, genre)

    finally:
        os.remove(temp_file_path)
