from fastapi import APIRouter, HTTPException
from typing import List, Optional
from database import get_db_connection
from models import Grade, GradeCreate

router = APIRouter(prefix="/grades", tags=["grades"])

@router.get("/", response_model=List[Grade])
def get_grades(position: Optional[str] = None):
    """Получить все грейды с фильтром по должности"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            if position:
                cur.execute("SELECT * FROM grades WHERE position = %s ORDER BY grade", (position,))
            else:
                cur.execute("SELECT * FROM grades ORDER BY position, grade")
            
            grades = cur.fetchall()
            return grades

@router.post("/", response_model=Grade)
def create_grade(grade_data: GradeCreate):
    """Создать новый грейд"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO grades (grade, position, grade_name)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (grade_data.grade, grade_data.position, grade_data.grade_name))
            
            new_grade = cur.fetchone()
            conn.commit()
            
            return new_grade

@router.get("/employees/{employee_id}/grade/", response_model=dict)
def get_employee_grade(employee_id: int):
    """Получить грейд сотрудника"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Сначала проверяем существование сотрудника
            cur.execute("SELECT id, name, position, last_review_date, grade_id FROM employees WHERE id = %s", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            current_grade = None
            if employee['grade_id']:
                cur.execute("SELECT grade, position, grade_name FROM grades WHERE id = %s", (employee['grade_id'],))
                grade_info = cur.fetchone()
                if grade_info:
                    current_grade = {
                        "grade_id": employee['grade_id'],
                        "grade": grade_info['grade'],
                        "position": grade_info['position'],
                        "grade_name": grade_info['grade_name']
                    }
            
            return {
                "employee_id": employee['id'],
                "name": employee['name'],
                "position": employee['position'],
                "current_grade": current_grade,
                "last_review_date": employee['last_review_date']
            }