# app/routers/employees.py

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from database import get_db_connection
from models import Achievement, EmployeeAchievement, EmployeeCreate, Employee, EmployeeWithProjects, ReviewRequest

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=List[Employee])
def get_employees():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT e.*, COALESCE(SUM(bc.delta), 0) AS bcoins, COALESCE(SUM(rc.delta), 0) AS rcoins
                        FROM employees AS e
                        LEFT JOIN blue_rating AS bc ON bc.employee_id=e.id
                        LEFT JOIN red_rating AS rc ON rc.employee_id=e.id
                        GROUP BY e.id
                        ORDER BY e.id""")
            employees = cur.fetchall()
            return employees
        
@router.get("/{employee_id}/achievements/", response_model=List[Achievement])
def get_employee_achievements(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("""
                SELECT a.* 
                FROM achievements a
                JOIN employees_achievements ea ON a.id = ea.achievement_id
                WHERE ea.employee_id = %s
                ORDER BY a.name
            """, (employee_id,))
            achievements = cur.fetchall()
            return achievements

@router.get("/{employee_id}/", response_model=EmployeeWithProjects)
def get_employee(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT e.*, COALESCE(SUM(bc.delta), 0) AS bcoins, COALESCE(SUM(rc.delta), 0) AS rcoins
                        FROM employees AS e
                        LEFT JOIN blue_rating AS bc ON bc.employee_id=e.id
                        LEFT JOIN red_rating AS rc ON rc.employee_id=e.id
                        WHERE e.id = %s
                        GROUP BY e.id""", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("""
                SELECT p.*, ep.job_start, ep.job_end, ep.position as project_position
                FROM employees_projects ep
                JOIN projects p ON ep.project_id = p.id
                WHERE ep.employee_id = %s
                ORDER BY ep.job_start
            """, (employee_id,))
            projects = cur.fetchall()
            
            employee["projects"] = projects
            employee["current_project"] = projects[-1] if projects else None
            return employee

@router.get("/{employee_id}/project_history/", response_model=List[dict])
def get_employee_project_history(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("""
                SELECT 
                    p.id as project_id,
                    p.name as project_name,
                    ep.job_start as start_date,
                    ep.job_end as end_date,
                    ep.position as position
                FROM employees_projects ep
                JOIN projects p ON ep.project_id = p.id
                WHERE ep.employee_id = %s
                ORDER BY ep.job_start ASC
            """, (employee_id,))
            
            project_history = cur.fetchall()
            return project_history

@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employees (name, employed_since, position)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (employee.name, employee.employed_since, employee.position))
            new_employee = cur.fetchone()
            return new_employee

@router.put("/{employee_id}/", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE employees 
                SET name = %s, employed_since = %s, position = %s
                WHERE id = %s
                RETURNING *
            """, (employee.name, employee.employed_since, employee.position, employee_id))
            updated_employee = cur.fetchone()
            if not updated_employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            return updated_employee

@router.delete("/{employee_id}/")
def delete_employee(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees_projects WHERE employee_id = %s", (employee_id,))
            cur.execute("DELETE FROM employees WHERE id = %s RETURNING id", (employee_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Employee not found")
            return {"message": "Employee deleted successfully"}
        
@router.post("/{employee_id}/achievements/{achievement_id}/", response_model=EmployeeAchievement, status_code=status.HTTP_201_CREATED)
def assign_achievement_to_employee(employee_id: int, achievement_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT id FROM achievements WHERE id = %s", (achievement_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Achievement not found")
            
            cur.execute("""
                SELECT id FROM employees_achievements 
                WHERE employee_id = %s AND achievement_id = %s
            """, (employee_id, achievement_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Achievement already assigned to this employee")
            
            cur.execute("""
                INSERT INTO employees_achievements (employee_id, achievement_id)
                VALUES (%s, %s)
                RETURNING *
            """, (employee_id, achievement_id))
            
            new_assignment = cur.fetchone()
            conn.commit()
            return new_assignment

@router.delete("/{employee_id}/achievements/{achievement_id}/")
def remove_achievement_from_employee(employee_id: int, achievement_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM employees_achievements 
                WHERE employee_id = %s AND achievement_id = %s
                RETURNING id
            """, (employee_id, achievement_id))
            
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Achievement not found for this employee")
            
            conn.commit()
            return {"message": "Achievement removed from employee"}


# COURSES

@router.get("/{employee_id}/courses/", response_model=List[dict])
def get_employee_courses(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("""
                SELECT 
                    c.*,
                    ec.course_started,
                    ec.course_completed,
                    ec.id as enrollment_id
                FROM courses_employees ec
                JOIN courses c ON ec.course_id = c.id
                WHERE ec.employee_id = %s
                ORDER BY ec.course_started DESC
            """, (employee_id,))
            
            courses = cur.fetchall()
            return courses
###ревью
@router.post("/{employee_id}/review/")
def update_employee_review(employee_id: int, review_data: Optional[ReviewRequest] = None):
    """Обновить дату последнего ревью и/или грейд сотрудника"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование сотрудника
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            # Если указан grade_id, проверяем его существование
            if review_data and review_data.grade_id:
                cur.execute("SELECT id FROM grades WHERE id = %s", (review_data.grade_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Grade not found")
            
            # Обновляем данные
            if review_data and review_data.grade_id:
                cur.execute("""
                    UPDATE employees 
                    SET last_review_date = CURRENT_TIMESTAMP, grade_id = %s
                    WHERE id = %s
                """, (review_data.grade_id, employee_id))
            else:
                cur.execute("""
                    UPDATE employees 
                    SET last_review_date = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (employee_id,))
            
            conn.commit()
            
            return {
                "message": "Review updated successfully",
                "employee_id": employee_id,
                "last_review_date": datetime.now(),
                "grade_id": review_data.grade_id if review_data else None
            }