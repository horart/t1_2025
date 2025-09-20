from pydantic import BaseModel
from typing import Optional, Dict, Any


class SurveyBase(BaseModel):
    id: int
    content_json: Dict[str, Any]
    module: str


class SurveyCreate(BaseModel):
    content_json: Dict[str, Any]
    module: str


class Survey(SurveyBase):

    class Config:
        from_attributes = True


class RespondersBase(BaseModel):
    answers_json: Dict[str, Any]
    quality: int



class RespondersCreate(RespondersBase):
    pass


class Responders(BaseModel):
    quality: int
    answers_json: Dict[str, Any]


    class Config:
        from_attributes = True