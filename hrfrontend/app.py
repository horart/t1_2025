from flask import Flask, render_template, redirect
from datetime import datetime
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return redirect("/hrdashboard")


@app.route('/hrchat')
def chat():
    return render_template('hrchat.html', title="chat")

@app.route('/hrdashboard')
def dashboard():

    return render_template('hrdashboard.html', title="dashboard")

@app.route('/hremployees')
def employees():
    workers = [{
        "employed_since": "2023-01-15T10:00:00Z",
        "id": 1,
        "name": "John Doe Updated",
        "position": "Lead Developer",
        "bcoins":100,
        "projects": [
            {
                "description": "Обновленный корпоративный сайт",
                "id": 1,
                "job_end": None,
                "job_start": "2024-01-15T09:00:00Z",
                "name": "Веб-сайт Updated",
                "project_position": "налитик"
            }
        ]
    }]
    return render_template('hremployees.html', title="employees", workers=workers)


@app.route('/userlk/<worker_id>')
def userlk(worker_id):
    this_worker = {
        "employed_since": "2023-01-15T10:00:00Z",
        "id": 1,
        "name": "John Doe Updated",
        "position": "Lead Developer",
        "rcoins": 228,
        "projects": [
            {
                "description": "Обновленный корпоративный сайт",
                "id": 1,
                "job_end": None,
                "job_start": "2024-01-15T09:00:00Z",
                "name": "еб-сайт Updated",
                "project_position": "налитик"
            }
        ]
    }
    skills = [{"id": 1, "name": "python", "value": 9.4}]

    return render_template('userlk.html', title="userlk", this_worker=this_worker, skills=skills)


@app.route('/projects')
def projects():
    projs = [
    {
        "description": "Обновленный корпоративный сайт",
        "id": 1,
        "name": "Dеб-сайт Updated",
        "employers":[],
        'employers_len':2
    },
    {
        "description": "Для теста",
        "id": 3,
        "name": "Тестовый проект",
        "employers": [],
        'employers_len': 3
    }
    ]
    # для каждого проекта надо запросить участников
    # for i in projs:
    #     projs['employers'] = requests.get()
    #     projs['employers_len'] = len(projs['employers'])
    return render_template('projects.html', title="projects", projects=projs)


if __name__ == '__main__':
    app.run(debug=True)