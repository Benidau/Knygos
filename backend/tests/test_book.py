

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_create_book_unauthorized():
    response = client.post("/books/", json={
        "title": "Test book",
        "author": "Test author",
        "rating": 5
    })
    
    assert response.status_code == 401




def test_create_book_with_invalid_token():
    bad_headers = {"Authorization": "Bearer blogas_tokenas_123"}
    
    payload = {
        "title": "Blogas testas",
        "author": "Testuotojas",
        "description": "Apibudinimas",
        "category": "Kat",
        "rating": 5
    }
    response = client.post("/books/", json=payload, headers=bad_headers)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"