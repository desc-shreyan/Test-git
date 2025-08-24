from fastapi import FastAPI
from pymongo import MongoClient
import os

# Create FastAPI app
app = FastAPI(title="FastAPI + MongoDB Demo")

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017/")  # default inside Docker
client = MongoClient(MONGO_URL)
db = client["Studentdb"]          # database
students_collection = db["Students"]  # collection

# Helper function
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "grade": student["grade"]
    }

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI + MongoDB working 🚀"}

# Create student
@app.post("/students")
def create_student(student: dict):
    result = students_collection.insert_one(student)
    new_student = students_collection.find_one({"_id": result.inserted_id})
    return student_helper(new_student)

# Get all students
@app.get("/students")
def get_students():
    return [student_helper(s) for s in students_collection.find()]
