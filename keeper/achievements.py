# app/routers/achievements.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import get_db_connection
from models import AchievementCreate, Achievement, EmployeeAchievement

router = APIRouter(prefix="/achievements", tags=["Achievements"])

@router.get("/", response_model=List[Achievement])
def get_achievements():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM achievements ORDER BY id")
            achievements = cur.fetchall()
            return achievements

@router.get("/employees/{employee_id}/", response_model=List[Achievement])
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

@router.post("/employees/{employee_id}/{achievement_id}", response_model=EmployeeAchievement, status_code=status.HTTP_201_CREATED)
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

@router.delete("/employees/{employee_id}/{achievement_id}")
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

@router.post("/", response_model=Achievement, status_code=status.HTTP_201_CREATED)
def create_achievement(achievement: AchievementCreate):
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

@router.put("/{achievement_id}", response_model=Achievement)
def update_achievement(achievement_id: int, achievement: AchievementCreate):
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

@router.delete("/{achievement_id}")
def delete_achievement(achievement_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees_achievements WHERE achievement_id = %s", (achievement_id,))
            cur.execute("DELETE FROM achievements WHERE id = %s RETURNING id", (achievement_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Achievement not found")
            conn.commit()
            return {"message": "Achievement deleted successfully"}