import psycopg2
import psycopg2._psycopg

from .models import SkillModel

class DataManager:
    conn: psycopg2._psycopg.connection
    def __init__(self, conn: psycopg2._psycopg.connection):
        self.conn = conn

    def fetch_user_projects(self, employee_id: int):
        projects = 1 #####