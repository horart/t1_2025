import psycopg2
import psycopg2._psycopg
import numpy as np
import psycopg2.extras

from .models import SkillModel

class DataManager:
    conn: psycopg2._psycopg.connection
    def __init__(self, conn: psycopg2._psycopg.connection):
        self.conn = conn
    
    def patch_skills(self, employee_id: int, skills_by_id: dict[int, int]):
        with self.conn.cursor() as cur:
            # Fetch current vector and updated_at (if needed for optimistic locking, etc.)
            cur.execute("""
                SELECT skills
                FROM employees_skills
                WHERE employee_id = %s
                FOR UPDATE  -- Optional: prevents race conditions
            """, (employee_id,))
            row = cur.fetchone()
            
            if not row:
                cur.execute("SELECT COUNT(id) FROM skills")
                dim = cur.fetchone()[0]
                current_vector = np.full(dim, 5.0, dtype=np.float32)
                cur.execute("INSERT INTO employees_skills (employee_id, updated_at, skills) VALUES (%s, NOW(), %s)",
                             (employee_id, current_vector.tolist()))

            # Deserialize vector (assuming it's stored as a pgvector type)
            else:
                current_vector = np.array(eval(row[0]))  # Convert to numpy array for easy manipulation

            # Apply updates: vector[i] = vector[i] + (val - vector[i]) * 0.2
            for skill_id, val in skills_by_id.items():
                # skill_id should be 1-based index? Adjust if your vector is 0-based.
                # PostgreSQL arrays are 1-indexed, but pgvector stores as 0-indexed numpy-like array.
                idx = skill_id
                if idx < 0 or idx >= len(current_vector):
                    raise IndexError(f"Skill ID {skill_id} out of vector bounds")

                current_vector[idx] += (val - current_vector[idx]) * 0.2

            # Update the row with new vector
            cur.execute("""
                UPDATE employees_skills
                SET skills = %s, updated_at = NOW()
                WHERE employee_id = %s
            """, (current_vector.tolist(), employee_id))
            cur.execute("""
                INSERT INTO public.employees_skills_history
                (employee_id, skills, created_at)
                VALUES(%s, %s, NOW());
            """, (employee_id, current_vector.tolist()))

    def get_skills(self, employee_id: int):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, name FROM skills")
            skills = cur.fetchall()
            
            cur.execute("SELECT skills FROM employees_skills WHERE employee_id = %s", (employee_id,))
            employee_skills_string = cur.fetchone()['skills']
            employee_skills_vector = np.array(eval(employee_skills_string))
            result = []
            for skill in skills:
                result.append(
                    SkillModel(id=skill['id'], 
                    name=skill['name'],
                    value=employee_skills_vector[skill['id']])
                )

        return result