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
###courses
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    hardness: int = Field(ge=1, le=3, description="Сложность: 1-легкий, 2-средний, 3-сложный")

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

class EmployeeCourseBase(BaseModel):
    course_id: int
    course_started: Optional[datetime] = Field(default_factory=datetime.now)
    course_completed: Optional[datetime] = None

class EmployeeCourseCreate(EmployeeCourseBase):
    pass

class EmployeeCourse(EmployeeCourseBase):
    id: int
    employee_id: int
    
    class Config:
        from_attributes = True

###courses

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

#endpoints of courses (begin)
# GET /courses/ - все курсы
@app.get("/courses/", response_model=List[Course])
def get_courses():
    """Получить все курсы"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM courses ORDER BY name")
            courses = cur.fetchall()
            return courses

# GET /courses/{id} - конкретный курс
@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int):
    """Получить курс по ID"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
            course = cur.fetchone()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            return course

# POST /courses/ - создать курс
@app.post("/courses/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    """Создать новый курс"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO courses (name, description, hardness)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (course.name, course.description, course.hardness))
            new_course = cur.fetchone()
            conn.commit()
            return new_course

# PUT /courses/{id} - обновить курс
@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course: CourseCreate):
    """Обновить курс"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE courses 
                SET name = %s, description = %s, hardness = %s
                WHERE id = %s
                RETURNING *
            """, (course.name, course.description, course.hardness, course_id))
            updated_course = cur.fetchone()
            if not updated_course:
                raise HTTPException(status_code=404, detail="Course not found")
            conn.commit()
            return updated_course

# DELETE /courses/{id} - удалить курс
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    """Удалить курс"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Сначала удаляем связи с сотрудниками
            cur.execute("DELETE FROM courses_employees WHERE course_id = %s", (course_id,))
            # Затем удаляем сам курс
            cur.execute("DELETE FROM courses WHERE id = %s RETURNING id", (course_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Course not found")
            conn.commit()
            return {"message": "Course deleted successfully"}

# GET /courses/{id}/employees - сотрудники курса
@app.get("/courses/{course_id}/employees", response_model=List[dict])
def get_course_employees(course_id: int):
    """Получить всех сотрудников на курсе"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Course not found")
            
            cur.execute("""
                SELECT 
                    e.*,
                    ec.course_started,
                    ec.course_completed,
                    ec.id as enrollment_id
                FROM courses_employees ec
                JOIN employees e ON ec.employee_id = e.id
                WHERE ec.course_id = %s
                ORDER BY e.name
            """, (course_id,))
            
            employees = cur.fetchall()
            return employees

# GET /employees/{id}/courses/ - курсы сотрудника
@app.get("/employees/{employee_id}/courses/", response_model=List[dict])
def get_employee_courses(employee_id: int):
    """Получить все курсы сотрудника"""
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

# POST /employees/{id}/courses/ - записать на курс
@app.post("/employees/{employee_id}/courses/", response_model=EmployeeCourse, status_code=status.HTTP_201_CREATED)
def enroll_employee_to_course(employee_id: int, course_data: EmployeeCourseCreate):
    """Записать сотрудника на курс"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT id FROM courses WHERE id = %s", (course_data.course_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Course not found")
            
            cur.execute("""
                SELECT id FROM courses_employees 
                WHERE employee_id = %s AND course_id = %s
            """, (employee_id, course_data.course_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Employee already enrolled in this course")
            
            cur.execute("""
                INSERT INTO courses_employees (employee_id, course_id, course_started, course_completed)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (employee_id, course_data.course_id, course_data.course_started, course_data.course_completed))
            
            enrollment = cur.fetchone()
            conn.commit()
            return enrollment

# POST /employees/{id}/courses/{id}/complete/ - завершить курс
@app.post("/employees/{employee_id}/courses/{course_id}/complete/", response_model=EmployeeCourse)
def complete_employee_course(employee_id: int, course_id: int):
    """Отметить курс как завершенный для сотрудника"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Course not found")
            
            cur.execute("""
                SELECT id, course_completed 
                FROM courses_employees 
                WHERE employee_id = %s AND course_id = %s
            """, (employee_id, course_id))
            
            enrollment = cur.fetchone()
            if not enrollment:
                raise HTTPException(status_code=404, detail="Employee is not enrolled in this course")
            
            if enrollment['course_completed'] is not None:
                raise HTTPException(status_code=400, detail="Course already completed")
            
            cur.execute("""
                UPDATE courses_employees 
                SET course_completed = CURRENT_TIMESTAMP
                WHERE employee_id = %s AND course_id = %s
                RETURNING *
            """, (employee_id, course_id))
            
            updated_enrollment = cur.fetchone()
            conn.commit()
            return updated_enrollment
#endpoints of courses (end)

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