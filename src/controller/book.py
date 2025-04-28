
from fastapi import HTTPException
from src.db import get_session
from src.schemas.book import BookCreateSchema
from src.crud.book import BookCRUD
from src.schemas.pagination.pagination import PageParams

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