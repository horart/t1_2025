# app/routers/projects.py

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from database import get_db_connection
from models import ProjectCreate, Project, ProjectWithEmployees, EmployeeProject

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[Project])
def get_projects_list():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects ORDER BY id")
            projects = cur.fetchall()
            return projects

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO projects (name, description)
                VALUES (%s, %s)
                RETURNING *
            """, (project.name, project.description))
            new_project = cur.fetchone()
            conn.commit()
            return new_project

@router.get("/{project_id}/", response_model=ProjectWithEmployees)
def get_project(project_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
            project = cur.fetchone()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            
            cur.execute("""
                SELECT e.*, ep.job_start, ep.job_end, ep.position as project_position
                FROM employees_projects ep
                JOIN employees e ON ep.employee_id = e.id
                WHERE ep.project_id = %s
                ORDER BY ep.job_start
            """, (project_id,))
            employees = cur.fetchall()
            
            project["employees"] = employees
            return project

@router.get("/{project_id}/employees/", response_model=List[dict])
def get_project_employees(project_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Project not found")
            
            cur.execute("""
                SELECT e.*, ep.job_start, ep.job_end, ep.position as project_position, ep.id as assignment_id
                FROM employees_projects ep
                JOIN employees e ON ep.employee_id = e.id
                WHERE ep.project_id = %s
                ORDER BY e.name
            """, (project_id,))
            employees = cur.fetchall()
            return employees

@router.get("/{project_id}/employees/{employee_id}", response_model=dict)
def get_project_employee(project_id: int, employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT e.*, ep.job_start, ep.job_end, ep.position as project_position, ep.id as assignment_id
                FROM employees_projects ep
                JOIN employees e ON ep.employee_id = e.id
                WHERE ep.project_id = %s AND ep.employee_id = %s
            """, (project_id, employee_id))
            assignment = cur.fetchone()
            
            if not assignment:
                raise HTTPException(status_code=404, detail="Employee not found on this project")
            
            return assignment

class AssignEmployeeRequest(BaseModel):
    position: str
    job_start: datetime = Field(default_factory=datetime.now)
    job_end: Optional[datetime] = None

@router.post("/{project_id}/employees/{employee_id}", response_model=EmployeeProject, status_code=status.HTTP_201_CREATED)
def assign_employee_to_project(
    project_id: int, 
    employee_id: int, 
    request: AssignEmployeeRequest
):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Project not found")
            
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("""
                SELECT id FROM employees_projects 
                WHERE project_id = %s AND employee_id = %s
            """, (project_id, employee_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Employee already assigned to this project")
            
            cur.execute("""
                INSERT INTO employees_projects (employee_id, project_id, job_start, job_end, position)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """, (employee_id, project_id, request.job_start, request.job_end, request.position))
            
            new_assignment = cur.fetchone()
            conn.commit()
            return new_assignment

@router.put("/{project_id}", response_model=Project)
def update_project(project_id: int, project: ProjectCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE projects 
                SET name = %s, description = %s
                WHERE id = %s
                RETURNING *
            """, (project.name, project.description, project_id))
            updated_project = cur.fetchone()
            if not updated_project:
                raise HTTPException(status_code=404, detail="Project not found")
            conn.commit()
            return updated_project

@router.delete("/{project_id}")
def delete_project(project_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees_projects WHERE project_id = %s", (project_id,))
            cur.execute("DELETE FROM projects WHERE id = %s RETURNING id", (project_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Project not found")
            conn.commit()
            return {"message": "Project deleted successfully"}