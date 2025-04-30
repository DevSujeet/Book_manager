from fastapi import HTTPException
from psycopg2 import IntegrityError
from sqlalchemy import and_, asc
from src.crud.base_curd import BaseCRUD
from src.models.book_summary import BookSummary
from src.schemas.book_summary import BookSummaryCreate


class BookSummaryCRUD(BaseCRUD):
    def create_book_summary(self, book_summary:BookSummaryCreate):
        try:
            book_summary_obj = BookSummary(**book_summary.model_dump(exclude={}))
            self.db_session.add(book_summary_obj)
            self.db_session.flush()
            self.db_session.commit()
            self.db_session.refresh(book_summary_obj)
            return book_summary_obj
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
        # Handle SQLite unique constraint violation
            if "UNIQUE constraint failed" in str(e.orig):
                print("Unique constraint failed: book summary already exists.")
                raise HTTPException(status_code=400, detail="book summary already exists")
            
            # Catch other IntegrityErrors and re-raise with a generic error
            raise HTTPException(status_code=500, detail="Internal Server Error")
        except Exception as e:
            # This will catch any unexpected exceptions that are not specifically caught by the above blocks
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def update_book_summary(self, book_id: str, summary: str, genre: str):
        '''
        Update the book summary and genre for a specific book.
        based on the book_id.
        '''
        if not book_id:
            raise HTTPException(status_code=400, detail="Book ID must be provided")
        if not summary:
            raise HTTPException(status_code=400, detail="Summary must be provided")
        if not genre:
            raise HTTPException(status_code=400, detail="Genre must be provided")
        filters = [BookSummary.book_id == book_id]

        book_summary = self.db_session.query(BookSummary).filter(BookSummary.book_id == book_id).first()
        if not book_summary:
            raise HTTPException(status_code=404, detail="Book summary not found")
        
        book_summary.book_summary = summary
        book_summary.genre = genre
        self.db_session.commit()
        return book_summary