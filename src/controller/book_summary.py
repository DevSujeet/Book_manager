

from fastapi import HTTPException
from src.schemas.pagination.pagination import PageParams
from src.db import get_session
from src.crud.book_summary import BookSummaryCRUD

def all_book_summary(user_id:str, page_params:PageParams):
    with get_session() as session:
        books = BookSummaryCRUD(db_session=session).get_all_summary(page_params=page_params)
        return books
    
def get_book_summary_by_id(user_id:str, id:str):
    with get_session() as session:
        book = BookSummaryCRUD(db_session=session).get_book_summary_by_id(id=id)
        if not book:
            raise HTTPException(status_code=404, detail="Book summary not found")
        return book
    
def get_book_summary_by_book_id(user_id:str, book_id:str):
    with get_session() as session:
        book = BookSummaryCRUD(db_session=session).get_book_summary_by_book_id(book_id=book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book summary not found")
        return book
    
def get_book_summary_by_user_id(user_id:str):
    with get_session() as session:
        books = BookSummaryCRUD(db_session=session).get_book_summary_by_user_id(user_id=user_id)
        if not books:
            return []
        return books