from typing import List
from fastapi import FastAPI
import psycopg2
import os
import re

import common.llmclient as llmclient
from .prompts import EMPLOYEE_PROMPT, HR_PROMPT
from .models import ChatPromptModel, ChatResponseModel
from .data_manager import DataManager
from .mcp import process_employee_prompt, process_hr_prompt


app = FastAPI()

connection = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5437),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'changeme'),
    database=os.getenv('POSTGRES_DATABASE', 'keeperdb'),
)
connection.autocommit = True
data_manager = DataManager(connection)
hr_to_context = {}
employee_to_context = {}

@app.post("/employee/{id}/prompt/")
def review(id: int, input: ChatPromptModel) -> ChatResponseModel:
    if 'id' not in employee_to_context:
        employee_to_context = llmclient.GenerativeLLM(EMPLOYEE_PROMPT, save_context=True)
    
    process_prompt(employee_to_context[id], input.body)
    output = employee_to_context[id].prompt(input.body)

    return ChatResponseModel(response=output)

@app.post("/hr/{id}prompt/")
def selfreview(review_model: ReviewRequestModel) -> ReviewResponseModel:
    return ReviewResponseModel(review=self_review_client.prompt(review_model.body))

@app.get("/employees/{id}/skills/", response_model=List[SkillModel])
def get_skills(id: int):
    return data_manager.get_skills(id)