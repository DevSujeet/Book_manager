from sqlalchemy import TIMESTAMP, CheckConstraint, Column, String, Integer, ForeignKey, Text, func
from sqlalchemy.orm import relationship
import uuid
from src.db import Base


class UserBookReview(Base):
    __tablename__ = 'user_book_review'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    book_id = Column(String(36), ForeignKey('book.book_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_review = Column(Text, nullable=True)
    rating_given = Column(Integer, nullable=True, 
                           doc="Rating must be between 1 and 5 if provided.")
    submitted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint('rating_given BETWEEN 1 AND 5', name='check_rating_given_range'),
    )
