
import io
from fastapi.testclient import TestClient

def test_create_book_without_file(client: TestClient):
    response = client.post("/book", data={
        "title": "Book Without File",
        "author": "Author",
        "isbn": "0001",
        "publisher": "Test Publisher",
        "publication_year": 2024,
        "genre": "Test Genre",
        "language": "English",
        "pages": 120,
        "summary": "This is a test summary"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book Without File"
    assert "book_id" in data

