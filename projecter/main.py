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
    port=os.getenv('POSTGRES_PORT', 5437),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'changeme'),
    database=os.getenv('POSTGRES_DATABASE', 'keeperdb'),
)
connection.autocommit = True
data_manager = DataManager(connection)
llm_embedder = llmclient.LLMEmbedder()

@app.get("/employees/{id}/relevant-projects/")
def get_alike_projects(id: int):
    users_projects = requests.get(f'http://keeper/employees/{id}/projects_history/').json()
    descriptions = [i['description'] for i in users_projects]
    embeddings = llm_embedder.embed(descriptions)
    embeddings = [i.embedding for i in embeddings.data]
    similar_projects = {}
    for mbd in embeddings:
        project_datas = data_manager.get_most_similar_projects(mbd, 5)
        for project in project_datas:
            if project['id'] not in similar_projects:
                similar_projects[project['id']] = project
                similar_projects[project['id']]['dist'] = 1 - project['dist']
            else:
                similar_projects[project['id']]['dist'] += 1 - project['dist']

    sorted_project_kv = sorted(similar_projects, key=lambda kv: kv[1]['dist'], reverse=True)
    sorted_project_kv = sorted_project_kv[:5]
    return [kv[1] for kv in sorted_project_kv]

@app.get("/projects/cv-matching")
def get_cv_matching_projects(cv: str):
    embedding = llm_embedder.embed(cv).data[0].embedding
    most_similar_projects = data_manager.get_most_similar_projects(embedding, 10)
    return most_similar_projects