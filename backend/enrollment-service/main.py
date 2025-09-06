

from fastapi import FastAPI, Form
from commands import EnrollCommand, DropCommand
from transaction_manager import TransactionManager
from sys import path as sys_path
import os
sys_path.append(os.path.abspath("../../user-service/src"))
sys_path.append(os.path.abspath("../../course-service/src"))
from user_service import UserService
from courseService import CourseService

user_service = UserService()
course_service = CourseService()

app = FastAPI()

@app.post("/enroll")
async def enroll(student_id: str = Form(...), course_id: str = Form(...)):
    manager = TransactionManager.get_instance()
    manager.begin()
    try:
        cmd = EnrollCommand(user_service, course_service, student_id, course_id)
        manager.execute(cmd)
        manager.commit()
        return {"success": True, "message": f"Student {student_id} enrolled in course {course_id}!"}
    except Exception as e:
        manager.rollback()
        return {"success": False, "message": f"Error: {e}"}


@app.get('/enroll')
async def enroll(userid : str = Form(...)):
    print(userid)
    return {"success":True , "message":"from entroll"}