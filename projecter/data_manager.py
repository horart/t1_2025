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
                SELECT id, name, desc, (embedding <=> %s::vector) as dist
                FROM projects
                ORDER BY dist ASC
                LIMIT %s""", (project_embedding, limit))
            
            return cur.fetchall()