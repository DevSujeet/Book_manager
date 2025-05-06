
from fastapi import HTTPException, UploadFile
from src.db import get_session
from src.schemas.book import BookCreateSchema
from src.crud.book import BookCRUD
from src.crud.book_summary import BookSummaryCRUD
from src.schemas.book_summary import BookSummaryCreate
from src.schemas.pagination.pagination import PageParams
from src.utilities.pdf_reader import extract_text_from_pdf
from src.config.log_config import logger
from src.services.gen_ai_service import generate_summary_and_genre
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
        print("Creating book entry")
        book_obj = BookCRUD(db_session=session).create_book_entry(book=book)
        if not book_obj:
            raise HTTPException(status_code=400, detail="Book creation failed")
        
        # create a book summary entry
        # book_obj.book_id is the primary key of the book
        # and is used to create the book summary
        summary_sch = BookSummaryCreate(
            book_id=book_obj.get("book_id"),
            book_rating=None,
            book_review_summary=None,
            book_summary=None,
            genre=None
        )
        _ = BookSummaryCRUD(db_session=session).create_book_summary(book_summary=summary_sch)


        return book_obj
    

def delete_book_by_id(user_id:str, book_id:str):
    with get_session() as session:
        book = BookCRUD(db_session=session).delete_book_by_id(id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    

async def process_pdf_summary(book_id: str, file_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_file.flush()
        temp_file_path = temp_file.name

    try:
        text = extract_text_from_pdf(temp_file_path)
        ai_result = await generate_summary_and_genre(text)

        response_content = ai_result.get("response", "")
        logger.info(f"AI response for book_id {book_id}: {response_content}")
        if not response_content:
            logger.error(f"Empty response from AI service for book_id: {book_id}")
            raise ValueError("Empty response received from AI service")

        try:
            ai_response = json.loads(response_content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for book_id {book_id}: {e}")
            raise ValueError(f"Failed to decode JSON from AI response: {e}") from e

        summary = ai_response.get("summary")
        genre = ai_response.get("genre")

        with get_session() as session:
            BookCRUD(db_session=session).update_book_summary_genre(book_id, summary, genre)
            BookSummaryCRUD(db_session=session).update_book_summary(book_id=book_id, summary=summary, genre=genre)
            logger.info(f"Book summary and genre updated for book_id: {book_id}")

    finally:
        os.remove(temp_file_path)

# async def process_pdf_summary(book_id: str, file: UploadFile):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
#         temp_file.write(await file.read())
#         temp_file_path = temp_file.name

#     try:
#         text = extract_text_from_pdf(temp_file_path)
#         ai_result = await generate_summary_and_genre(text)
#         ai_response = json.loads(ai_result["response"])

#         summary = ai_response.get("summary")
#         genre = ai_response.get("genre")

#         # Update the book record
#         with get_session() as session:
            
#             BookCRUD(db_session=session).update_book_summary_genre(book_id, summary, genre)
#             # update the book summary and genre for a specific book

#             BookSummaryCRUD(db_session=session).update_book_summary(book_id=book_id, summary=summary, genre=genre)
#     finally:
#         os.remove(temp_file_path)
