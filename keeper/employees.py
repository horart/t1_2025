# app/routers/employees.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from database import get_db_connection
from models import EmployeeCreate, Employee, EmployeeWithProjects

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=List[Employee])
def get_employees():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees ORDER BY id")
            employees = cur.fetchall()
            return employees

@router.get("/{employee_id}/", response_model=EmployeeWithProjects)
def get_employee(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT *, bcoins, rcoins FROM employees WHERE id = %s", (employee_id,))
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
            return employee

@router.get("/{employee_id}/project_history", response_model=List[dict])
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
                ORDER BY ep.job_start DESC
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

@router.put("/{employee_id}", response_model=Employee)
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

@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees_projects WHERE employee_id = %s", (employee_id,))
            cur.execute("DELETE FROM employees WHERE id = %s RETURNING id", (employee_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Employee not found")
            return {"message": "Employee deleted successfully"}