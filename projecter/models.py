from pydantic import BaseModel
from typing import Optional

class ReviewRequestModel(BaseModel):
    body: str
    employee_id: int
    reviewer: Optional[int]
    

class ReviewResponseModel(BaseModel):
    review: str

class SkillModel(BaseModel):
    id: int
    name: str
    value: float