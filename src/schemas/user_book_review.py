from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field

class UserBookReviewBase(BaseModel):
    rating_given: Optional[Annotated[int, Field(ge=1, le=5)]] = None
    user_review: Optional[str] = None

class UserBookReviewCreate(UserBookReviewBase):
    user_id: int
    book_id: int

class UserBookReviewUpdate(UserBookReviewBase):
    pass

class UserBookReviewResponse(UserBookReviewBase):
    id: int
    user_id: int
    book_id: int
    submitted_at: datetime
    
    class Config:
        from_attributes = True
