from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_get_facilities():
    # Test location search
    response = client.get("/api/facilities?lga=Kanke")
    assert response.status_code == 200
    data = response.json()
    assert "facilities" in data
    assert type(data["facilities"]) is list
    assert len(data["facilities"]) > 0
    assert "Kanke" in data["facilities"][0]["lga"]

def test_get_benefits():
    # Test benefit category search
    response = client.get("/api/benefits?category=Maternal")
    assert response.status_code == 200
    data = response.json()
    assert "benefits" in data
    assert type(data["benefits"]) is list
    assert len(data["benefits"]) > 0

@patch("app.api.chat.generate_chat_response")
def test_chat_endpoint(mock_generate_chat_response):
    # Mock the AI so we don't actually hit Gemini during automated tests (saves money/time)
    mock_generate_chat_response.return_value = "This is a mock answer from the AI."
    
    response = client.post("/api/chat/", json={
        "message": "Where can I get free malaria treatment?",
        "lga": "Kanke",
        "ward": "Namu"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is a mock answer from the AI."
    assert data["lga_searched"] == "Kanke"
    assert data["ward_searched"] == "Namu"
    
    # Ensure it rejects missing messages
    bad_response = client.post("/api/chat/", json={
        "lga": "Kanke"
    })
    assert bad_response.status_code == 422 # FastAPI validation error for missing field

@patch("app.database.supabase_client.supabase.table")
def test_feedback_endpoint(mock_supabase_table):
    # Mock supabase insert so we don't write to DB during tests
    mock_execute = mock_supabase_table.return_value.insert.return_value.execute
    mock_execute.return_value.data = [{"id": 1, "message": "Test issue"}]
    
    response = client.post("/api/feedback/", json={
        "message": "I was charged for malaria drugs",
        "facility_name": "PHC Namu",
        "lga": "Kanke",
        "ward": "Namu"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
