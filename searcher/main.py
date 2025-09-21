from typing import List
from fastapi import FastAPI
import psycopg2
import os

import common.llmclient as llmclient
from .prompts import EMPLOYEE_PROMPT, HR_PROMPT
from .models import ChatPromptModel, ChatResponseModel
from .data_manager import DataManager
from .mcp import process_employee_prompt


app = FastAPI()

hr_to_context = {}
employee_to_context = {}

@app.post("/employee/{id}/prompt/")
def review(id: int, input: ChatPromptModel) -> ChatResponseModel:
    global employee_to_context
    if 'id' not in employee_to_context:
        employee_to_context[id] = llmclient.GenerativeLLM(EMPLOYEE_PROMPT, save_context=True)
    
    process_employee_prompt(id, employee_to_context[id], input.body)
    output = employee_to_context[id].prompt(input.body)

    return ChatResponseModel(response=output)
