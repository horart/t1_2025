import re

import common.llmclient

def process_employee_prompt(client: common.llmclient.GenerativeLLM, prompt: str):
    while True:
        output = client.prompt("<WhoAmI who='system' />" + prompt)
        system_query_tags = re.findall(r"<SystemQuery[^>]*/>", output)
        if system_query_tags:
            for tag in system_query_tags:
                params = re.findall(r"(\w+)='([^']*)'", tag)
                param_dict = {key: value for key, value in params}
                client.prompt(f"<SystemResult>{query(**param_dict)}</SystemResult>")

def query(**kwargs):
    if kwargs.get('type') == 'search' and kwargs.get('domain') == 'learning':
        courses = search_for_courses()
    elif kwargs.get('type') == 'search' and kwargs.get('domain') == 'jobs':
        jobs = search_for_jobs()
    elif kwargs.get('type') == 'enroll':
        enroll_user_for_course()
    else:
        return "Unknown query type or domain."
    
def search_for_courses():
    return 