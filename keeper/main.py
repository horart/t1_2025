from fastapi import FastAPI, HTTPException, Depends, status
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

# Pydantic модели для ачивок
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int
    
    class Config:
        from_attributes = True

class EmployeeAchievementBase(BaseModel):
    employee_id: int
    achievement_id: int

class EmployeeAchievementCreate(EmployeeAchievementBase):
    pass

class EmployeeAchievement(EmployeeAchievementBase):
    id: int
    
    class Config:
        from_attributes = True

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



@app.get("/employees/{employee_id}/project_history", response_model=List[dict])
def get_employee_project_history(employee_id: int):
    """Получить историю проектов сотрудника"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование сотрудника
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            # Получаем историю проектов сотрудника
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

#begin of new endpoints
@app.get("/projects/", response_model=List[Project])
def get_projects_list():
    """Получить список всех проектов"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects ORDER BY id")
            projects = cur.fetchall()
            return projects

@app.post("/projects/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):
    """Создать новый проект"""
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

@app.get("/projects/{project_id}", response_model=ProjectWithEmployees)
def get_project(project_id: int):
    """Получить проект по ID"""
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

@app.get("/projects/{project_id}/employees/", response_model=List[dict])
def get_project_employees(project_id: int):
    """Получить всех сотрудников проекта"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование проекта
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

@app.get("/projects/{project_id}/employees/{employee_id}", response_model=dict)
def get_project_employee(project_id: int, employee_id: int):
    """Получить конкретного сотрудника на проекте"""
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

# Pydantic модель для создания назначения
class AssignEmployeeRequest(BaseModel):
    position: str
    job_start: datetime = Field(default_factory=datetime.now)
    job_end: Optional[datetime] = None

@app.post("/projects/{project_id}/employees/{employee_id}", response_model=EmployeeProject, status_code=status.HTTP_201_CREATED)
def assign_employee_to_project(
    project_id: int, 
    employee_id: int, 
    request: AssignEmployeeRequest
):
    """Привязать сотрудника к проекту"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование проекта и сотрудника
            cur.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Project not found")
            
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            # Проверяем, не назначен ли уже сотрудник на проект
            cur.execute("""
                SELECT id FROM employees_projects 
                WHERE project_id = %s AND employee_id = %s
            """, (project_id, employee_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Employee already assigned to this project")
            
            # Создаем назначение
            cur.execute("""
                INSERT INTO employees_projects (employee_id, project_id, job_start, job_end, position)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """, (employee_id, project_id, request.job_start, request.job_end, request.position))
            
            new_assignment = cur.fetchone()
            conn.commit()
            return new_assignment
#end of new endpoints

#endpoints of achievments (begin)
# Эндпоинты для ачивок
@app.get("/achievements/", response_model=List[Achievement])
def get_achievements():
    """Получить все типы ачивок"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM achievements ORDER BY id")
            achievements = cur.fetchall()
            return achievements

@app.get("/employees/{employee_id}/achievements/", response_model=List[Achievement])
def get_employee_achievements(employee_id: int):
    """Получить все ачивки сотрудника"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование сотрудника
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            # Получаем ачивки сотрудника
            cur.execute("""
                SELECT a.* 
                FROM achievements a
                JOIN employees_achievements ea ON a.id = ea.achievement_id
                WHERE ea.employee_id = %s
                ORDER BY a.name
            """, (employee_id,))
            achievements = cur.fetchall()
            return achievements

@app.post("/employees/{employee_id}/achievements/{achievement_id}", response_model=EmployeeAchievement, status_code=status.HTTP_201_CREATED)
def assign_achievement_to_employee(employee_id: int, achievement_id: int):
    """Назначить ачивку сотруднику"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование сотрудника и ачивки
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT id FROM achievements WHERE id = %s", (achievement_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Achievement not found")
            
            # Проверяем, не назначена ли уже ачивка
            cur.execute("""
                SELECT id FROM employees_achievements 
                WHERE employee_id = %s AND achievement_id = %s
            """, (employee_id, achievement_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Achievement already assigned to this employee")
            
            # Назначаем ачивку
            cur.execute("""
                INSERT INTO employees_achievements (employee_id, achievement_id)
                VALUES (%s, %s)
                RETURNING *
            """, (employee_id, achievement_id))
            
            new_assignment = cur.fetchone()
            conn.commit()
            return new_assignment

@app.delete("/employees/{employee_id}/achievements/{achievement_id}")
def remove_achievement_from_employee(employee_id: int, achievement_id: int):
    """Удалить ачивку у сотрудника"""
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

# Дополнительные CRUD операции для ачивок
@app.post("/achievements/", response_model=Achievement, status_code=status.HTTP_201_CREATED)
def create_achievement(achievement: AchievementCreate):
    """Создать новую ачивку"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO achievements (name, description, image_path)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (achievement.name, achievement.description, achievement.image_path))
            new_achievement = cur.fetchone()
            conn.commit()
            return new_achievement

@app.put("/achievements/{achievement_id}", response_model=Achievement)
def update_achievement(achievement_id: int, achievement: AchievementCreate):
    """Обновить ачивку"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE achievements 
                SET name = %s, description = %s, image_path = %s
                WHERE id = %s
                RETURNING *
            """, (achievement.name, achievement.description, achievement.image_path, achievement_id))
            updated_achievement = cur.fetchone()
            if not updated_achievement:
                raise HTTPException(status_code=404, detail="Achievement not found")
            conn.commit()
            return updated_achievement

@app.delete("/achievements/{achievement_id}")
def delete_achievement(achievement_id: int):
    """Удалить ачивку"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Сначала удаляем связи с сотрудниками
            cur.execute("DELETE FROM employees_achievements WHERE achievement_id = %s", (achievement_id,))
            # Затем удаляем саму ачивку
            cur.execute("DELETE FROM achievements WHERE id = %s RETURNING id", (achievement_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Achievement not found")
            conn.commit()
            return {"message": "Achievement deleted successfully"}
#endpoints of achievments (end)
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