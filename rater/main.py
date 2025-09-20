from typing import List
from fastapi import FastAPI
import psycopg2
import os
import re

import common.llmclient as llmclient
from .prompts import REVIEW_PROMPT, SELF_REVIEW_PROMPT
from .models import ReviewRequestModel, ReviewResponseModel, SkillModel
from .skillfinder import SkillFinder
from .xmlparser import parse_xml
from .data_manager import DataManager


app = FastAPI()

review_client = llmclient.GenerativeLLM(REVIEW_PROMPT)
self_review_client = llmclient.GenerativeLLM(SELF_REVIEW_PROMPT)
connection = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5437),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'changeme'),
    database=os.getenv('POSTGRES_DATABASE', 'postgres'),
)
connection.autocommit = True
skill_finder = SkillFinder(connection)
data_manager = DataManager(connection)

@app.post("/review/")
def review(review_model: ReviewRequestModel) -> ReviewResponseModel:
    output = review_client.prompt(review_model.body)
    output = re.findall(r'<[Ss]kills>.*</[Ss]kills>', output, re.DOTALL)[0]
    skills_by_name = parse_xml(output)
    skills_by_id = skill_finder.normalize_skills(skills_by_name)
    data_manager.patch_skills(review_model.employee_id, skills_by_id)
    return ReviewResponseModel(review=output)

@app.post("/self-review/")
def selfreview(review_model: ReviewRequestModel) -> ReviewResponseModel:
    return ReviewResponseModel(review=self_review_client.prompt(review_model.body))

@app.get("/employees/{id}/skills/", response_model=List[SkillModel])
def get_skills(id: int):
    return data_manager.get_skills(id)