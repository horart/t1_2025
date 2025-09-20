from typing import List
from fastapi import FastAPI
import psycopg2
import os
import requests

from .data_manager import DataManager
from common import llmclient

app = FastAPI()

connection = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5435),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'changeme'),
    database=os.getenv('POSTGRES_DATABASE', 'postgres'),
)
connection.autocommit = True
data_manager = DataManager(connection)
llm_embedder = llmclient.LLMEmbedder()

@app.get("/employees/{id}/relevant-projects/")
def get_alike_projects(id: int):
    users_projects = requests.get(f'http://keeper/employees/{id}/projects/').json()
    