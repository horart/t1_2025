from pydantic import BaseModel
from typing import Optional

class EmployeePromptModel(BaseModel):
    employee_id: int
    body: str
    reqid: Optional[int]

class HRPromptModel(BaseModel):
    hr_id: int
    body: str
    reqid: Optional[int]