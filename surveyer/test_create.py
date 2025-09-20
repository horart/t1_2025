import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is defined in main.py

client = TestClient(app)

# Sample data for creating a survey
sample_survey_data = {
    "content_json": {
        "title": "Тестовый опрос",
        "questions": [
            {"question": "What is your favorite color?", "type": "text"},
            {"question": "How old are you?", "type": "number"}
        ]
    },
    "module": "test_module"
}

def test_create_survey():
    response = client.post("/surveys/", json=sample_survey_data)
    assert response.status_code == 200
    created_survey = response.json()
    assert "id" in created_survey
    assert created_survey["content_json"] == sample_survey_data["content_json"]
    assert created_survey["module"] == sample_survey_data["module"]

if __name__ == "__main__":
    pytest.main()