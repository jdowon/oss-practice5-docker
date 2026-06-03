import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
JSON_FILE = "courses.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def load_courses():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_courses(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/courses")
def get_courses():
    return load_courses()

@app.post("/courses")
def create_course(course: Course):
    try:
        data = load_courses()
        data.append(course.dict())
        save_courses(data)
        return {"message": "Success", "inserted": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))