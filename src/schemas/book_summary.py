from typing import Optional, Annotated
from pydantic import BaseModel, Field
from src.enum.preference_enum import GenreEnum


class BookSummaryBase(BaseModel):
    book_rating: Optional[float] = None
    book_review_summary: Optional[str] = None
    book_summary: Optional[str] = None
    genre: Optional[GenreEnum] = None

class BookSummaryCreate(BookSummaryBase):
    book_id: int  # required during create

class BookSummaryUpdate(BookSummaryBase):
    pass

class BookSummaryResponse(BookSummaryBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True
