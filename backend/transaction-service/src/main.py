# main.py
# Example usage of the Transaction Service with user and course services
from commands import EnrollCommand, DropCommand
from transaction_manager import TransactionManager

# Import the actual service classes
from sys import path as sys_path
import os
sys_path.append(os.path.abspath("../../user-service/src"))
sys_path.append(os.path.abspath("../../course-service/src"))
from services.user_service import UserService
from services.courseService import CourseService

user_service = UserService()
course_service = CourseService()

# Example: Enroll a student in a course atomically
student_id = "S001"
course_id = "CS101"

manager = TransactionManager.get_instance()
manager.begin()
try:
    cmd = EnrollCommand(user_service, course_service, student_id, course_id)
    manager.execute(cmd)
    manager.commit()
    print(f"Student {student_id} enrolled in course {course_id}!")
except Exception as e:
    print(f"Error: {e}. Rolling back...")
    manager.rollback()
