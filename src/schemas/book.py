from pydantic import BaseModel, Field
from typing import Optional
import uuid

class BookCreateSchema(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    publisher: Optional[str]
    publication_year: Optional[int]
    genre: Optional[str]
    language: Optional[str]
    pages: Optional[int]
    summary: Optional[str]

    class Config:
        from_attributes = True
        # orm_mode = True

class BookResponseSchema(BookCreateSchema):
    book_id: str 


# class ReviewCreateSchema(BaseModel):
#     book_id: str
#     user_id: str
#     review_text: Optional[str]
#     rating: int

#     class Config:
#         from_attributes = True

# class ReviewResponseSchema(ReviewCreateSchema):
#     id: str