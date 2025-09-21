import re

import common.llmclient
import requests

def process_employee_prompt(uid: int, client: common.llmclient.GenerativeLLM, prompt: str):
        output = client.prompt("<WhoAmI who='user' />" + prompt)
        system_query_tags = re.findall(r"<SystemQuery[^>]*/>", output)
        if system_query_tags:
            for tag in system_query_tags:
                params = re.findall(r"(\w+)='([^']*)'", tag)
                param_dict = {key: value for key, value in params}
                return client.prompt(f"<WhoAmI who='system' /><SystemResult>{query(uid, **param_dict)}</SystemResult>")
        else:
            return output

def query(uid, **kwargs):
    if kwargs.get('type') == 'search' and kwargs.get('domain') == 'learning':
        courses = search_for_courses(uid, "\n".join(f'{i[0]} is {i[1]}' for i in kwargs.items()))
        return str(courses)
    elif kwargs.get('type') == 'search' and kwargs.get('domain') == 'jobs':
        jobs = search_for_projects(uid, "\n".join(f'{i[0]} is {i[1]}' for i in kwargs.items()))
    else:
        return "There is no data is the system apparantly"
    
def search_for_courses(uid, cv):
    courses_for_man = requests.get(f"http://projecter:8000/employees/{uid}/relevant-courses").json()
    courses_for_cv = requests.post("http://projecter:8000/courses/cv-matching/", json={"cv": cv}).json()
    return str(courses_for_cv) + str(courses_for_man)

def search_for_projects(uid, cv):
    courses_for_man = requests.get(f"http://projecter:8000/employees/{uid}/relevant-projects").json()
    courses_for_cv = requests.post("http://projecter:8000/projects/cv-matching/", json={"cv": cv}).json()
    return str(courses_for_man) + str(courses_for_cv)