from fastapi import FastAPI
from database import engine, Base
import surveys, responders

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Survey API", version="1.0.0")

# Подключаем роутеры
app.include_router(surveys.router, prefix="/surveys", tags=["surveys"])
app.include_router(responders.router, prefix="/surveys", tags=["responders"])

@app.get("/")
def root():
    return {"message": "Survey API is running"}
