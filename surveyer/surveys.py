from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from .models import Survey
from schemas import SurveyCreate
from schemas import Survey as SurveySch

router = APIRouter()

@router.post("/", response_model=SurveySch)
def create_survey(survey: SurveyCreate, db: Session = Depends(get_db)):
    # Создаем объект БД без указания id
    db_survey = Survey(

        content_json=survey.content_json,
        module=survey.module
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


@router.delete("/{survey_id}")
def delete_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    db.delete(survey)
    db.commit()
    return {"message": "Survey deleted successfully"}


@router.get("/{survey_id}")
def get_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    return survey.content_json

@router.get("/", response_model=List[SurveySch])
def get_all_surveys(db: Session = Depends(get_db)):
    surveys = db.query(Survey).all()
    return surveys