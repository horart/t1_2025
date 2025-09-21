import os
import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST", "keeper")
DB_NAME = os.getenv("DB_NAME", "keeperdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "changeme")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    cursor_factory=RealDictCursor
)

conn.autocommit = True

@contextmanager
def get_db_connection():
    """Return the global connection — simple and reusable"""
    yield conn