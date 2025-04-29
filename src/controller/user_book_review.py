
from src.schemas.user_book_review import UserBookReviewCreate, UserBookReviewUpdate
from src.schemas.pagination.pagination import PageParams
from fastapi import HTTPException
from src.db import get_session
from src.crud.user_book_review import UserBookReviewCRUD

def create_user_book_review(review:UserBookReviewCreate, user_id:str):
    """
    Create a new user book review entry.
    """
    with get_session() as session:
        user_obj = UserBookReviewCRUD(db_session=session).create_user_book_reivew_entry(review=review)
        if not user_obj:
            raise HTTPException(status_code=400, detail="user book review creation failed")
        return user_obj

def get_user_book_review_by_id(user_id:str, id:str):
    """
    Get a user book review by ID.
    """
    with get_session() as session:
        book = UserBookReviewCRUD(db_session=session).get_user_book_review_by_id(id=id)
        if not book:
            raise HTTPException(status_code=404, detail="user book review not found")
        return book
    
def update_user_book_review(user_id:str, id:str):
    """
    Update the book review if required or inititated by the user.    
    """
    with get_session() as session:
        book = UserBookReviewCRUD(db_session=session).update_user_book_review(id=id)
        if not book:
            raise HTTPException(status_code=404, detail="user book review not found")
        return book
    pass 

def delete_user_book_review(user_id:str, id:str):
    """
    Delete a user book review by ID.
    """
    with get_session() as session:
        book = UserBookReviewCRUD(db_session=session).delete_user_review_by_id(id=id)
        if not book:
            raise HTTPException(status_code=404, detail="user book review not found")
        return book