# tests/test_books.py

from src.schemas.book import BookCreateSchema
from src.crud.book import BookCRUD
import uuid

def test_create_and_get_book(db_session):
    book_in = BookCreateSchema(
        title="Test Book",
        author="John Doe",
        isbn="12345",
        publisher="XYZ",
        publication_year=2020,
        genre="Fiction",
        language="English",
        pages=100,
        summary="A test book"
    )

    book_crud = BookCRUD(db_session=db_session)
    created = book_crud.create_book_entry(book=book_in)
    
    assert created["title"] == "Test Book"
    assert "book_id" in created

    fetched = book_crud.get_book_by_id(id=created["book_id"])
    assert fetched.title == "Test Book"
    assert fetched.author == "John Doe"

def test_delete_book(db_session):
    book_in = BookCreateSchema(
        title="To Delete",
        author="John Doe",
        isbn="12345",
        publisher="XYZ",
        publication_year=2020,
        genre="Fiction",
        language="English",
        pages=100,
        summary="A test book"
    )
    book_crud = BookCRUD(db_session=db_session)
    created = book_crud.create_book_entry(book=book_in)
    
    deleted = book_crud.delete_book_by_id(id=created["book_id"])
    assert deleted.title == "To Delete"

    # Now check it is actually gone
    try:
        book_crud.get_book_by_id(id=created["book_id"])
        assert False  # should not reach here
    except Exception as e:
        assert "not found" in str(e.detail)
