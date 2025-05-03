from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, asc
from src.models.book import BookData
from src.schemas.book import BookCreateSchema, BookResponseSchema
from src.crud.base_curd import BaseCRUD
from src.schemas.pagination.pagination import PageParams, paginate

class BookCRUD(BaseCRUD):
    def all_book(self, page_params:PageParams):
        query = self.db_session.query(BookData).order_by(asc(BookData.title))
        return paginate(page_params=page_params, query=query, ResponseSchema=BookResponseSchema, model=BookData)
        

    def get_book_by_id(self, id:str):
        if not id:
            raise HTTPException(status_code=400, detail="Book ID must be provided")
    
        filters = [BookData.book_id == id]
        query = self.db_session.query(BookData).filter(and_(*filters))
        book = query.first()
        if book:
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    
    def create_book_entry(self, book: BookCreateSchema):
        try:
            book_obj = BookData(**book.model_dump(exclude={}))
            self.db_session.add(book_obj)
            print(f'create_book in crud post {book_obj}')
            self.db_session.flush()
            self.db_session.commit()
            self.db_session.refresh(book_obj)
            print(f'book is created {book_obj.__dict__}')
            book_dict = book_obj.__dict__.copy()
            book_dict.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal state
            return book_dict
        except IntegrityError as e:
            print(f"IntegrityError: {e}")  # Log the full exception
            print(f"Exception details: {e.orig}")  # Print out the underlying database exception details

            # Handle SQLite unique constraint violation
            if "UNIQUE constraint failed" in str(e.orig):
                print("Unique constraint failed: book_id already exists.")
                raise HTTPException(status_code=400, detail="book_id already exists")
            
            # Catch other IntegrityErrors and re-raise with a generic error
            raise HTTPException(status_code=500, detail="Internal Server Error")
        except Exception as e:
            # This will catch any unexpected exceptions that are not specifically caught by the above blocks
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def delete_book_by_id(self, id:str):
        book = self.get_book_by_id(id=id)
        if book:
            self.db_session.delete(book)
            self.db_session.commit()
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")
        
    def update_book_summary_genre(self, book_id: str, summary: str, genre: str):
        book = self.get_book_by_id(id=book_id)
        if book:
            book.summary = summary
            book.genre = genre
            self.db_session.commit()
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")
        