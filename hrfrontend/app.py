from flask import Flask, render_template, redirect, request
from datetime import datetime
import requests
from settings import KEEPER_URL, PROJECTER_URL, RATER_URL, SEARCHER_URL, SURVEYER_URL
import json


app = Flask(__name__)

@app.route('/')
def index():
    return redirect("/hrdashboard")


@app.route('/hrchat')
def chat():
    return render_template('hrchat.html', title="chat")


@app.route('/hrdashboard')
def dashboard():
    projs = requests.get(f'{PROJECTER_URL}/projects/hr/1').json()
    proj_len = len(projs)
    peoplesinpr = 0
    for i in projs:
        projs['employers_len'] = len(projs['employees'])
        peoplesinpr += len(projs['employees'])
    return render_template('hrdashboard.html', title="dashboard", proj_len=proj_len, )


@app.route('/hremployees')
def employees():
    workers = []
    projs = requests.get(f'{PROJECTER_URL}/projects/hr/1').json()
    for i in projs:
        workers = workers + projs['employees']
    return render_template('hremployees.html', title="employees", workers=workers)


@app.route('/userlk/<worker_id>')
def userlk(worker_id):
    this_worker = requests.get(f'{KEEPER_URL}/employees/{worker_id}/').json()
    skills = requests.get(f'{KEEPER_URL}/employees/{worker_id}/skills/').json()

    return render_template('userlk.html', title="userlk", this_worker=this_worker, skills=skills)


@app.route('/projects')
def projects():
    projs = requests.get(f'{PROJECTER_URL}/projects/hr/1').json()

    for i in projs:
        projs['employers_len'] = len(projs['employees'])
    return render_template('projects.html', title="projects", projects=projs)

@app.route('/api/user/prompt')
def prompt():
    request_data = request.get_data()
    return json.loads(requests.post(f"http://searcher:8000/hr/1/prompt/",data=request_data).json())["data"]



if __name__ == '__main__':
    app.run(debug=True)