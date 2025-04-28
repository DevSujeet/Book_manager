from fastapi import APIRouter, Depends
from fastapi.logger import logger
from src.schemas.user_book_review import UserBookReviewCreate, UserBookReviewResponse, UserBookReviewUpdate
from src.controller.user_book_review import create_user_book_review, get_user_book_review_by_id, update_user_book_review, delete_user_book_review
from src.config.configs import _db_settings

# from src.schema.book import Book
router = APIRouter(
    prefix="/user_book_review",
    tags=["book"]
)

@router.post('')
async def create_user_book_reivew(review:UserBookReviewCreate) -> UserBookReviewResponse:
    created_reivew = create_user_book_review(user_id="123", review=review)
    return created_reivew

@router.patch('')
async def update_user_book_review(review:UserBookReviewUpdate) -> UserBookReviewResponse:
    updated_reivew = update_user_book_review(user_id="123", review=review)
    return updated_reivew

@router.delete('')
async def delete_user_book_review(id:str) -> UserBookReviewResponse:
    deleted_reivew = delete_user_book_review(user_id="123", id=id)
    return deleted_reivew