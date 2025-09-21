# app/routers/achievements.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from database import get_db_connection
from models import AchievementCreate, Achievement, EmployeeAchievement

router = APIRouter(prefix="/achievements", tags=["Achievements"])

@router.get("/", response_model=List[Achievement])
def get_achievements():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM achievements ORDER BY id")
            achievements = cur.fetchall()
            return achievements
        
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