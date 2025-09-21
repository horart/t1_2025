from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

from login import auth_required
from settings import KEEPER_URL, PROJECTER_URL, RATER_URL, SEARCHER_URL, SURVEYER_URL

app.secret_key = 't1-super-secret'

@app.route('/')
@auth_required
def index(uid):
    user = requests.get(f'{KEEPER_URL}/employees/{uid}/').json()
    courses = requests.get(f'{KEEPER_URL}/employees/{uid}/courses/').json()
    bcoins = user['bcoins']
    rcoins = user['rcoins']
    sitebar = bcoins * 100 / 100
    return render_template('index.html', title="Home", sitebar=sitebar, rcoins=rcoins, bcoins=bcoins, courses=courses)

@app.route('/analytics')
def analytics():
    this_worker = {
                        "employed_since": "2023-01-15T10:00:00Z",
                        "id": 1,
                        "name": "John Doe Updated",
                        "position": "Lead Developer",
                        "rcoins": 228,
                        "projects": [
                            {
                                "description": "бновленный корпоративный сайт",
                                "id": 1,
                                "job_end": None,
                                "job_start": "2024-01-15T09:00:00Z",
                                "name": "еб-сайт Updated",
                                "project_position": "налитик"
                            }
                        ]
                    }
    leaderboard = [
                    {
                        "employed_since": "2023-01-15T10:00:00Z",
                        "id": 1,
                        "name": "John Doe Updated",
                        "position": "Lead Developer",
                        "rcoins": 228,
                        "projects": [
                            {
                                "description": "бновленный корпоративный сайт",
                                "id": 1,
                                "job_end": None,
                                "job_start": "2024-01-15T09:00:00Z",
                                "name": "еб-сайт Updated",
                                "project_position": "налитик"
                            }
                        ]
                    },
                    {
                        "employed_since": "2023-01-15T10:00:00Z",
                        "id": 1,
                        "name": "Джони бой",
                        "position": "Lead Developer",
                        "rcoins": 228,
                        "projects": [
                            {
                                "description": "бновленный корпоративный сайт",
                                "id": 1,
                                "job_end": None,
                                "job_start": "2024-01-15T09:00:00Z",
                                "name": "еб-сайт Updated",
                                "project_position": "налитик"
                            }
                        ]
                    },
                    {
                        "employed_since": "2023-01-15T10:00:00Z",
                        "id": 1,
                        "name": "Васян Хохлов",
                        "position": "Lead Developer",
                        "rcoins": 228,
                        "projects": [
                            {
                                "description": "бновленный корпоративный сайт",
                                "id": 1,
                                "job_end": None,
                                "job_start": "2024-01-15T09:00:00Z",
                                "name": "еб-сайт Updated",
                                "project_position": "налитик"
                            }
                        ]
                    },
                    {
                        "employed_since": "2023-01-15T10:00:00Z",
                        "id": 1,
                        "name": "Павел Шуршало",
                        "position": "Lead Developer",
                        "rcoins": 228,
                        "projects": [
                            {
                                "description": "бновленный корпоративный сайт",
                                "id": 1,
                                "job_end": None,
                                "job_start": "2024-01-15T09:00:00Z",
                                "name": "еб-сайт Updated",
                                "project_position": "налитик"
                            }
                        ]
                    },
                    {
                        "employed_since": "2023-01-15T10:00:00Z",
                        "id": 1,
                        "name": "Антон Овертюн",
                        "position": "Lead Developer",
                        "rcoins": 228,
                        "projects": [
                            {
                                "description": "бновленный корпоративный сайт",
                                "id": 1,
                                "job_end": None,
                                "job_start": "2024-01-15T09:00:00Z",
                                "name": "еб-сайт Updated",
                                "project_position": "налитик"
                            }
                        ]
                    }
    ]
    awards = [
                    {
                        "description": "",
                        "id": 1,
                        "image_path": "/images/best-employee.png",
                        "name": "Количество проектов"
                    },
                    {
                        "description": "Award for best work",
                        "id": 1,
                        "image_path": "/images/best-employee.png",
                        "name": "Best worker"
                    },
                    {
                        "description": "Award for best work",
                        "id": 1,
                        "image_path": "/images/best-employee.png",
                        "name": "Best worker"
                    },
                    {
                        "description": "Award for best work",
                        "id": 1,
                        "image_path": "/images/best-employee.png",
                        "name": "Best worker"
                    }
    ]
    carier_path =[
    {
        "end_date": None,
        "position": "Аналитик",
        "project_id": 1,
        "project_name": "Веб-сайт Updated",
        "start_date": "2024-01-15T09:00:00Z"
    }
    ]
    # GET /employees/{id}/project-history/
    projects = [{"employee_id":22}]

    years_old_work = datetime.now().year - int(this_worker["employed_since"][:4])
    projects_len = len(projects)
    # GET / employees / {id} / project - history /
    return render_template('analytics.html', title="Analytics", leaderboard=leaderboard,
                            this_worker=this_worker, awards=awards, carier_path=carier_path, years_old_work=years_old_work,
                           projects_len=projects_len, carier_len=len(carier_path))

@app.route('/courses')
def courses():
    it_courses = [
        {
            "course_completed": None,
            "course_started": "2025-09-20T17:26:57.967585Z",
            "description": "Основы",
            "enrollment_id": 1,
            "hardness": 1,
            "id": 1,
            "name": "Python"
        }
    ]
    all_courses = [
    {
        "course_completed": None,
        "course_started": "2025-09-20T17:26:57.967585Z",
        "description": "Основы",
        "enrollment_id": 1,
        "hardness": 1,
        "id": 1,
        "name": "Python"
    }
    ]
    return render_template('courses.html', title="Courses", all_courses=all_courses, it_courses=it_courses)

@app.route('/market')
def market():
    this_worker = {
        "employed_since": "2023-01-15T10:00:00Z",
        "id": 1,
        "name": "John Doe Updated",
        "position": "Lead Developer",
        "rcoins": 228,
        "projects": [
            {
                "description": "бновленный корпоративный сайт",
                "id": 1,
                "job_end": None,
                "job_start": "2024-01-15T09:00:00Z",
                "name": "еб-сайт Updated",
                "project_position": "налитик"
            }
        ]
    }
    return render_template('market.html', title="Courses", rcoins=this_worker["rcoins"])

@app.route('/userlk')
def userlk():
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
    skills = [{"id":1, "name":"python", "value":9.4}]

    return render_template('userlk.html', title="userlk", this_worker=this_worker, skills=skills)



@app.route('/chat')
def chat():
    return render_template('chat.html', title="chat")


@app.route('/tests')
def test():
    return render_template('tests.html', title="test")




if __name__ == '__main__':
    app.run(debug=True)