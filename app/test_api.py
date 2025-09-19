import requests
import json

url = "http://localhost:8000/surveys/"
data = {
    "content_json": {
        "title": "Тестовый опрос",
        "questions": []
    },
    "module": "test_module"
}

data1 = {
    "quality":10,
    "answers_json": {"answers":["сиськи", "письки"]}
  
}

response = requests.get("http://localhost:8000/surveys/2/responders/2")
print(response.status_code)
print(response.content.decode("UTF-8"))