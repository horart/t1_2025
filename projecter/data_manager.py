from typing import List
import psycopg2
import psycopg2._psycopg
import psycopg2.extras

class DataManager:
    conn: psycopg2._psycopg.connection
    def __init__(self, conn: psycopg2._psycopg.connection):
        self.conn = conn

    def get_most_similar_projects(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, (embedding <=> %s::vector) as dist
                FROM projects
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_courses(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name, description, hardness, (embedding <=> %s::vector) as dist
                FROM courses
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
        
    def get_most_similar_vacancies(self, project_embedding: List[float], limit: int = 5):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT vacancies.id, vacancies.description, vacancies.position, projects.id as project_id, projects.description as project_description, (embedding <=> %s::vector) as dist
                FROM vacancies
                LEFT JOIN projects ON vacancies.project_id = projects.id
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()
