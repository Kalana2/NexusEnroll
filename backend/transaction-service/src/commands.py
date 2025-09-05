# commands.py
# Command pattern for atomic operations using user and course services
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class EnrollCommand(Command):
    def __init__(self, user_service, course_service, student_id, course_id):
        self.user_service = user_service
        self.course_service = course_service
        self.student_id = student_id
        self.course_id = course_id
        self._prev_course_state = None
        self._prev_user_state = None
        self.executed = False

    def execute(self):
        # Save previous state for rollback
        course = self.course_service.get_course(self.course_id)
        user = self.user_service.get_user(self.student_id)
        self._prev_course_state = course.copy() if hasattr(course, 'copy') else course.dict()
        self._prev_user_state = user.copy() if hasattr(user, 'copy') else user.dict()
        # Perform enrollment (simulate: update course and user)
        if course.current_enrollment >= course.total_capacity:
            raise Exception("Course is full")
        # Update course enrollment
        self.course_service.update_course_info(self.course_id, {"current_enrollment": course.current_enrollment + 1})
        # Optionally update user record (e.g., add course to student schedule)
        # self.user_service.update_user(self.student_id, {"...": ...})
        self.executed = True

    def undo(self):
        if self.executed:
            # Restore previous state
            self.course_service.update_course_info(self.course_id, self._prev_course_state)
            self.user_service.update_user(self.student_id, self._prev_user_state)
            self.executed = False

class DropCommand(Command):
    def __init__(self, user_service, course_service, student_id, course_id):
        self.user_service = user_service
        self.course_service = course_service
        self.student_id = student_id
        self.course_id = course_id
        self._prev_course_state = None
        self._prev_user_state = None
        self.executed = False

    def execute(self):
        course = self.course_service.get_course(self.course_id)
        user = self.user_service.get_user(self.student_id)
        self._prev_course_state = course.copy() if hasattr(course, 'copy') else course.dict()
        self._prev_user_state = user.copy() if hasattr(user, 'copy') else user.dict()
        if course.current_enrollment <= 0:
            raise Exception("No students to drop")
        self.course_service.update_course_info(self.course_id, {"current_enrollment": course.current_enrollment - 1})
        # Optionally update user record
        self.executed = True

    def undo(self):
        if self.executed:
            self.course_service.update_course_info(self.course_id, self._prev_course_state)
            self.user_service.update_user(self.student_id, self._prev_user_state)
            self.executed = False
