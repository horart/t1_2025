# app/routers/vacancies.py

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from .database import get_db_connection
from .models import Vacancy, VacancyCreate, VacancyWithDetails, VacancyStatusUpdate

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])

@router.get("/", response_model=List[VacancyWithDetails])
def get_vacancies(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    hr_id: Optional[int] = None
):
    """Получить вакансии с фильтрацией"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            query = """
                SELECT v.*, p.name as project_name, e.name as hr_name
                FROM vacancies v
                JOIN projects p ON v.project_id = p.id
                JOIN employees e ON v.hr_id = e.id
                WHERE 1=1
            """
            params = []
            
            if status:
                query += " AND v.status = %s"
                params.append(status)
            
            if project_id:
                query += " AND v.project_id = %s"
                params.append(project_id)
            
            if hr_id:
                query += " AND v.hr_id = %s"
                params.append(hr_id)
            
            query += " ORDER BY v.created_at DESC"
            
            cur.execute(query, params)
            vacancies = cur.fetchall()
            return vacancies

@router.get("/{vacancy_id}", response_model=VacancyWithDetails)
def get_vacancy(vacancy_id: int):
    """Получить вакансию по ID"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT v.*, p.name as project_name, e.name as hr_name
                FROM vacancies v
                JOIN projects p ON v.project_id = p.id
                JOIN employees e ON v.hr_id = e.id
                WHERE v.id = %s
            """, (vacancy_id,))
            
            vacancy = cur.fetchone()
            if not vacancy:
                raise HTTPException(status_code=404, detail="Vacancy not found")
            
            return vacancy

@router.post("/", response_model=Vacancy, status_code=status.HTTP_201_CREATED)
def create_vacancy(vacancy: VacancyCreate):
    """Создать новую вакансию"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Проверяем существование проекта
                cur.execute("SELECT id FROM projects WHERE id = %s", (vacancy.project_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Project not found")
                
                # Проверяем существование HR
                cur.execute("SELECT id FROM employees WHERE id = %s", (vacancy.hr_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="HR manager not found")
                
                cur.execute("""
                    INSERT INTO vacancies (project_id, hr_id, position, status)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, project_id, hr_id, position, status, created_at
                """, (vacancy.project_id, vacancy.hr_id, vacancy.position, vacancy.status or 'open'))
                
                new_vacancy = cur.fetchone()
                conn.commit()
                return new_vacancy
                
    except Exception as e:
        print(f"Error creating vacancy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{vacancy_id}", response_model=Vacancy)
def update_vacancy(vacancy_id: int, vacancy: VacancyCreate):
    """Обновить вакансию"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование вакансии
            cur.execute("SELECT id FROM vacancies WHERE id = %s", (vacancy_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Vacancy not found")
            
            # Проверяем существование проекта
            cur.execute("SELECT id FROM projects WHERE id = %s", (vacancy.project_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Project not found")
            
            # Проверяем существование HR
            cur.execute("SELECT id FROM employees WHERE id = %s", (vacancy.hr_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="HR manager not found")
            
            cur.execute("""
                UPDATE vacancies 
                SET project_id = %s, hr_id = %s, position = %s, status = %s
                WHERE id = %s
                RETURNING id, project_id, hr_id, position, status, created_at
            """, (vacancy.project_id, vacancy.hr_id, vacancy.position, vacancy.status, vacancy_id))
            
            updated_vacancy = cur.fetchone()
            conn.commit()
            return updated_vacancy

@router.patch("/{vacancy_id}/status", response_model=Vacancy)
def update_vacancy_status(vacancy_id: int, status_update: VacancyStatusUpdate):
    """Обновить статус вакансии"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE vacancies 
                SET status = %s
                WHERE id = %s
                RETURNING id, project_id, hr_id, position, status, created_at
            """, (status_update.status, vacancy_id))
            
            updated_vacancy = cur.fetchone()
            if not updated_vacancy:
                raise HTTPException(status_code=404, detail="Vacancy not found")
            
            conn.commit()
            return updated_vacancy

@router.delete("/{vacancy_id}")
def delete_vacancy(vacancy_id: int):
    """Удалить вакансию"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vacancies WHERE id = %s RETURNING id", (vacancy_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Vacancy not found")
            
            conn.commit()
            return {"message": "Vacancy deleted successfully"}

@router.get("/project/{project_id}", response_model=List[VacancyWithDetails])
def get_project_vacancies(project_id: int):
    """Получить все вакансии проекта"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем существование проекта
            cur.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Project not found")
            
            cur.execute("""
                SELECT v.*, p.name as project_name, e.name as hr_name
                FROM vacancies v
                JOIN projects p ON v.project_id = p.id
                JOIN employees e ON v.hr_id = e.id
                WHERE v.project_id = %s
                ORDER BY v.created_at DESC
            """, (project_id,))
            
            vacancies = cur.fetchall()
            return vacancies

@router.get("/debug/check-table")
def check_vacancies_table():
    """Проверить существование таблицы vacancies"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'vacancies'
                    ) as table_exists
                """)
                result = cur.fetchone()
                return {"table_exists": result['table_exists']}
    except Exception as e:
        return {"error": str(e)}