import uuid
from sqlalchemy import Column, TIMESTAMP, func, String, INT
from src.db import Base
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from sqlalchemy import ForeignKey
# from sqlalchemy.ext.declarative import declarative_base



class BookData(Base):
    __tablename__ = 'book'

    book_id = Column('book_id', String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    title = Column("title", String, nullable=True)
    author = Column("author", String, nullable=True)
    isbn = Column("isbn", String, nullable=True)
    publisher = Column("publisher", String, nullable=True)
    publication_year = Column("publication_year", INT, nullable=True)
    genre = Column("genre", String, nullable=True)
    language = Column("language", String, nullable=True)
    pages = Column("pages", INT, nullable=True)
    summary = Column("summary", String, nullable=True)
