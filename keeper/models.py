from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    employed_since: datetime
    position: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    bcoins: Optional[int] = 0 
    rcoins: Optional[int] = 0 
    
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
    
    class Config:
        from_attributes = True
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

class RatingCreate(BaseModel):
    delta: int
    reason: str

class EmployeeCourse(EmployeeCourseBase):
    id: int
    employee_id: int
    
    class Config:
        from_attributes = True

class Employee(EmployeeBase): ##ДЛЯ РЕЙТИНГА И БАЛАНСА
    id: int
    bcoins: int = 0  # ← Добавляем
    rcoins: int = 0  # ← Добавляем
    
    class Config:
        from_attributes = True

class ShopItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_rcoins: int
    image_path: Optional[str] = None
    category: Optional[str] = None

class ShopItemCreate(ShopItemBase):
    pass

class ShopItem(ShopItemBase):
    id: int
    is_available: bool
    
    class Config:
        from_attributes = True

class PurchaseRequest(BaseModel):
    employee_id: int
    quantity: int = 1

class RedCoinsUpdate(BaseModel):
    delta: int
    reason: str
###courses

class GradeBase(BaseModel):
    grade: int
    position: str
    grade_name: str

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    
    class Config:
        from_attributes = True

class ReviewRequest(BaseModel):
    grade_id: Optional[int] = None

class Employee(EmployeeBase):
    id: int
    bcoins: Optional[int] = 0 
    rcoins: Optional[int] = 0 
    last_review_date: Optional[datetime] = None
    grade_id: Optional[int] = None 
    
    class Config:
        from_attributes = True

# ProjectBase
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    hr_id: Optional[int] = None  # ← Добавляем

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    
    class Config:
        from_attributes = True

class AssignEmployeeRequest(BaseModel):
    position: str
    job_start: datetime = Field(default_factory=datetime.now)
    job_end: Optional[datetime] = None