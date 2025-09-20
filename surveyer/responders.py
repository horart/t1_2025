from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Responders
from schemas import RespondersCreate
from schemas import Responders as Responders_Sch


router = APIRouter()


@router.get("/{survey_id}/responders", response_model=List[int])
def get_responders(survey_id: int, db: Session = Depends(get_db)):
    responders = db.query(Responders).filter(Responders.survey_id == survey_id).all()
    return [resp.employee_id for resp in responders]


@router.get("/{survey_id}/responders/{employee_id}")
def get_responder_responses(survey_id: int, employee_id: int, db: Session = Depends(get_db)):
    responders = db.query(Responders).filter(Responders.employee_id == employee_id)
    responders = responders.filter(Responders.survey_id == survey_id).first()
    return [responders.quality, responders.answers_json]


@router.post("/{survey_id}/responders/{employee_id}", response_model=Responders_Sch)
def submit_response(survey_id: int, employee_id: int, response: RespondersCreate, db: Session = Depends(get_db)):
    db_response = Responders(

        employee_id=employee_id,
        survey_id=survey_id,
        answers_json=response.answers_json,
        quality=response.quality
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response