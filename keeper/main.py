from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from contextlib import contextmanager

app = FastAPI()

# Database connection settings from environment
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASS = os.getenv("DB_PASS", "mypassword")

# Pydantic models
class EmployeeBase(BaseModel):
    name: str
    employed_since: datetime
    position: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    
    class Config:
        from_attributes = True

class EmployeeProjectBase(BaseModel):
    employee_id: int
    project_id: int
    job_start: datetime
    job_end: Optional[datetime] = None
    position: str

class EmployeeProjectCreate(EmployeeProjectBase):
    pass

class EmployeeProject(EmployeeProjectBase):
    id: int
    
    class Config:
        from_attributes = True

class EmployeeWithProjects(Employee):
    projects: List[dict] = []

class ProjectWithEmployees(Project):
    employees: List[dict] = []

# Database connection helper
@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )
    try:
        yield conn
    finally:
        conn.close()

# Employees CRUD
@app.get("/employees", response_model=List[Employee])
def get_employees():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees ORDER BY id")
            employees = cur.fetchall()
            return employees

@app.get("/employees/{employee_id}", response_model=EmployeeWithProjects)
def get_employee(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Get employee
            cur.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            # Get employee's projects
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

@app.post("/employees", response_model=Employee)
def create_employee(employee: EmployeeCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employees (name, employed_since, position)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (employee.name, employee.employed_since, employee.position))
            new_employee = cur.fetchone()
            conn.commit()
            return new_employee

@app.put("/employees/{employee_id}", response_model=Employee)
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
            conn.commit()
            return updated_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # First delete from employees_projects to avoid foreign key constraint
            cur.execute("DELETE FROM employees_projects WHERE employee_id = %s", (employee_id,))
            cur.execute("DELETE FROM employees WHERE id = %s RETURNING id", (employee_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Employee not found")
            conn.commit()
            return {"message": "Employee deleted successfully"}

# Projects CRUD
@app.get("/projects", response_model=List[Project])
def get_projects():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects ORDER BY id")
            projects = cur.fetchall()
            return projects

@app.get("/projects/{project_id}", response_model=ProjectWithEmployees)
def get_project(project_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Get project
            cur.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
            project = cur.fetchone()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            
            # Get project's employees
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

@app.post("/projects", response_model=Project)
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

@app.put("/projects/{project_id}", response_model=Project)
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

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # First delete from employees_projects to avoid foreign key constraint
            cur.execute("DELETE FROM employees_projects WHERE project_id = %s", (project_id,))
            cur.execute("DELETE FROM projects WHERE id = %s RETURNING id", (project_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Project not found")
            conn.commit()
            return {"message": "Project deleted successfully"}

# Employee-Project assignments CRUD
@app.get("/assignments", response_model=List[EmployeeProject])
def get_assignments():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees_projects ORDER BY id")
            assignments = cur.fetchall()
            return assignments

@app.post("/assignments", response_model=EmployeeProject)
def create_assignment(assignment: EmployeeProjectCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if employee and project exist
            cur.execute("SELECT id FROM employees WHERE id = %s", (assignment.employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT id FROM projects WHERE id = %s", (assignment.project_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Project not found")
            
            cur.execute("""
                INSERT INTO employees_projects (employee_id, project_id, job_start, job_end, position)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """, (assignment.employee_id, assignment.project_id, assignment.job_start, 
                 assignment.job_end, assignment.position))
            new_assignment = cur.fetchone()
            conn.commit()
            return new_assignment

@app.put("/assignments/{assignment_id}", response_model=EmployeeProject)
def update_assignment(assignment_id: int, assignment: EmployeeProjectCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE employees_projects 
                SET employee_id = %s, project_id = %s, job_start = %s, job_end = %s, position = %s
                WHERE id = %s
                RETURNING *
            """, (assignment.employee_id, assignment.project_id, assignment.job_start, 
                 assignment.job_end, assignment.position, assignment_id))
            updated_assignment = cur.fetchone()
            if not updated_assignment:
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return updated_assignment

@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees_projects WHERE id = %s RETURNING id", (assignment_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return {"message": "Assignment deleted successfully"}

# Health check endpoints
@app.get("/")
def read_root():
    return {"message": "Employee and Project Management API"}

@app.get("/db-test")
def test_db():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW() as now;")
                result = cur.fetchone()
                return {"status": "success", "db_time": result["now"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}