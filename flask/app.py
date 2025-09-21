from flask import Flask
from flask import session, render_template, request, redirect, url_for
from datetime import datetime
import requests
import json

app = Flask(__name__)

# from login import auth_required
from settings import KEEPER_URL, PROJECTER_URL, RATER_URL, SEARCHER_URL, SURVEYER_URL

def auth_required(f):
    def wrapper(*args, **kwargs):
        if 'uid' not in session:
            return redirect(url_for('login'))
        return f(session['uid'], *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper



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
@auth_required
def analytics(uid):
    this_worker = requests.get(f'{KEEPER_URL}/employees/{uid}/').json()
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
    awards = requests.get(f'{KEEPER_URL}/employees/{uid}/achievements/').json()
    carier_path = [
    {
        "end_date": None,
        "position": "Аналитик",
        "project_id": 1,
        "project_name": "Веб-сайт Updated",
        "start_date": "2024-01-15T09:00:00Z"
    }]
    # carier_path = requests.get(f"{KEEPER_URL}/career-path/?name={this_worker['position']}").json()

    # GET /employees/{id}/project-history/
    projects = requests.get(f'{KEEPER_URL}/employees/{uid}/project_history/').json()

    years_old_work = datetime.now().year - int(this_worker["employed_since"][:4])
    projects_len = len(projects)
    # GET / employees / {id} / project - history /
    return render_template('analytics.html', title="Analytics", leaderboard=leaderboard,
                            this_worker=this_worker, awards=awards, carier_path=carier_path, years_old_work=years_old_work,
                           projects_len=projects_len, carier_len=len(carier_path))

@app.route('/courses')
@auth_required
def courses(uid):
    it_courses = requests.get(f'{KEEPER_URL}/employees/{uid}/courses/').json()
    all_courses = requests.get(f'{KEEPER_URL}/courses/').json()
    return render_template('courses.html', title="Courses", all_courses=all_courses, it_courses=it_courses)

@app.route('/market')
@auth_required
def market(uid):
    this_worker = requests.get(f'{KEEPER_URL}/employees/{uid}/').json()
    return render_template('market.html', title="Courses", rcoins=this_worker["rcoins"])

@app.route('/userlk')
@auth_required
def userlk(uid):
    this_worker = requests.get(f'{KEEPER_URL}/employees/{uid}/').json()
    skills = requests.get(f'{KEEPER_URL}/employees/{uid}/skills/').json()

    return render_template('userlk.html', title="userlk", this_worker=this_worker, skills=skills)



@app.route('/chat')
def chat():
    return render_template('chat.html', title="chat")


@app.route('/tests')
def ttt():
    return render_template('tests.html', title="tests")


@app.route('/api/user/prompt')
@auth_required
def prompt(uid):
    request_data = request.get_data()
    return json.loads(requests.post(f"http://searcher:8000/employee/{uid}/prompt/",data=request_data).json())["data"]


if __name__ == '__main__':
    app.run(debug=True)