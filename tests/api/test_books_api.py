
import io
from fastapi.testclient import TestClient
import src.db as db

# def test_create_book_without_file(client: TestClient):
#     response = client.post("/book", data={
#         "title": "Book Without File",
#         "author": "Author",
#         "isbn": "0001",
#         "publisher": "Test Publisher",
#         "publication_year": 2024,
#         "genre": "Test Genre",
#         "language": "English",
#         "pages": 120,
#         "summary": "This is a test summary"
#     })
#     assert response.status_code == 200
#     data = response.json()
#     assert data["title"] == "Book Without File"
#     assert "book_id" in data
#------------------------------------------------------------
# def test_create_book_without_file(client):
#     data = {
#         "title": "Book Without File",
#         "author": "Author",
#         "isbn": "0001",
#         "publisher": "Test Publisher",
#         "publication_year": "2024",
#         "genre": "action",
#         "language": "English",
#         "pages": "120",
#         "summary": "This is a test summary"
#     }

#     # Ensure multipart/form-data format by setting files, even if empty
#     response = client.post("/book", data=data, files={})

#     assert response.status_code == 200
#     assert response.json()["title"] == "Book Without File"
#---------------------------------------------------------------
# def test_create_book_without_file(client, db_session, monkeypatch):
#     # Patch get_session to return your test SQLite session
#     monkeypatch.setattr(db, "get_session", lambda: db_session)

#     data = {
#         "title": "Book Without File",
#         "author": "Author",
#         "isbn": "0001",
#         "publisher": "Test Publisher",
#         "publication_year": "2024",
#         "genre": "action",
#         "language": "English",
#         "pages": "120",
#         "summary": "This is a test summary"
#     }

#     response = client.post("/book", data=data, files={})
#     assert response.status_code == 200

# import src.crud.book as book_crud
import src.controller.book as book_service

def test_create_book_without_file(client, db_session, monkeypatch):
    # Route ➝ create_book_entry() (calls get_session) ➝ BookCRUD(db_session).create_book_entry()
    # So the get_session() is used inside create_book_entry()
    # Patch get_session to return your test SQLite session
    monkeypatch.setattr(book_service, "get_session", lambda: db_session)

    data = {
        "title": "Book Without File",
        "author": "Author",
        "isbn": "0001",
        "publisher": "Test Publisher",
        "publication_year": "2024",
        "genre": "action",
        "language": "English",
        "pages": "120",
        "summary": "This is a test summary"
    }

    response = client.post("/book", data=data, files={})
    assert response.status_code == 200