import psycopg2
import psycopg2._psycopg

class DataManager:
    conn: psycopg2._psycopg.connection
    def __init__(self, conn: psycopg2._psycopg.connection):
        self.conn = conn
    
    