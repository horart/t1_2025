# app/routers/courses.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from database import get_db_connection
from models import CourseCreate, Course, EmployeeCourse

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[Course])
def get_courses():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM courses ORDER BY name")
            courses = cur.fetchall()
            return courses

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
            course = cur.fetchone()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            return course

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
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

@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course: CourseCreate):
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

@router.delete("/{course_id}")
def delete_course(course_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM courses_employees WHERE course_id = %s", (course_id,))
            cur.execute("DELETE FROM courses WHERE id = %s RETURNING id", (course_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Course not found")
            conn.commit()
            return {"message": "Course deleted successfully"}

@router.get("/{course_id}/employees/", response_model=List[dict])
def get_course_employees(course_id: int):
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

@router.post("/{course_id}/employees/{employee_id}/", response_model=EmployeeCourse, status_code=status.HTTP_201_CREATED)
def enroll_employee_to_course(course_id: int, employee_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Course not found")
            
            cur.execute("""
                SELECT id FROM courses_employees 
                WHERE employee_id = %s AND course_id = %s
            """, (employee_id, course_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Employee already enrolled in this course")
            
            cur.execute("""
                INSERT INTO courses_employees (employee_id, course_id)
                VALUES (%s, %s)
                RETURNING *
            """, (employee_id, course_id))
            
            enrollment = cur.fetchone()
            conn.commit()
            return enrollment

@router.post("/{course_id}/employees/{employee_id}/complete/", response_model=EmployeeCourse)
def complete_employee_course(employee_id: int, course_id: int):
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