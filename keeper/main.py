from fastapi import FastAPI

import employees, projects, achievements, courses, rating

app = FastAPI(
    title="Employee & Project Management API",
    description="Modular FastAPI app with routers for employees, projects, achievements, courses, and rating/shop",
    version="1.0.0"
)

# Include routers
app.include_router(employees.router)
app.include_router(projects.router)
app.include_router(achievements.router)
app.include_router(courses.router)
app.include_router(rating.router)

@app.get("/")
def read_root():
    return {"message": "Employee and Project Management API"}

@app.get("/db-test")
def test_db():
    try:
        from database import get_db_connection
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW() as now;")
                result = cur.fetchone()
                return {"status": "success", "db_time": result["now"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}