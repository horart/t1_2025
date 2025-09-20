from sqlalchemy import Column, Integer, String, JSON, BigInteger
from database import Base


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    content_json = Column(JSON, nullable=False)
    module = Column(String, nullable=False)


class Responders(Base):
    __tablename__ = "responders"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    survey_id = Column(Integer, nullable=False)
    answers_json = Column(JSON, nullable=False)
    quality = Column(Integer, nullable=False)