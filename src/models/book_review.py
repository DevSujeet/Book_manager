from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
import uuid
from src.db import Base


class ReviewData(Base):
    __tablename__ = 'book_review'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    book_id = Column(String(36), ForeignKey('book.book_id'), nullable=False)
    user_id = Column(String(36), nullable=False)
    review_text = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)

    # Optional: SQLAlchemy relationship to BookData
    book = relationship("BookData", backref="reviews")