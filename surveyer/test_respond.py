import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is defined in main.py

client = TestClient(app)

# Sample data for creating a responder response
sample_response_data = {
    "answers_json": {"answers": ["сиськи", "письки"]},
    "quality": 10
}

# Sample survey ID and employee ID
sample_survey_id = 1
sample_employee_id = 1

def test_submit_response():
    response = client.post(f"/surveys/{sample_survey_id}/responders/{sample_employee_id}", json=sample_response_data)
    assert response.status_code == 200
    created_response = response.json()
    assert created_response["answers_json"] == sample_response_data["answers_json"]
    assert created_response["quality"] == sample_response_data["quality"]

def test_get_responders():
    # First, submit a response to ensure there is data to retrieve
    client.post(f"/surveys/{sample_survey_id}/responders/{sample_employee_id}", json=sample_response_data)
    
    response = client.get(f"/surveys/{sample_survey_id}/responders")
    assert response.status_code == 200
    responders = response.json()
    assert isinstance(responders, list)
    assert sample_employee_id in responders

def test_get_responder_responses():
    # First, submit a response to ensure there is data to retrieve
    client.post(f"/surveys/{sample_survey_id}/responders/{sample_employee_id}", json=sample_response_data)
    
    response = client.get(f"/surveys/{sample_survey_id}/responders/{sample_employee_id}")
    assert response.status_code == 200
    responder_responses = response.json()
    assert isinstance(responder_responses, list)
    assert responder_responses[0] == sample_response_data["quality"]
    assert responder_responses[1] == sample_response_data["answers_json"]

if __name__ == "__main__":
    pytest.main()