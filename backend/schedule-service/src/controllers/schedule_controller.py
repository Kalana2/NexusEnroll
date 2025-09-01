from src.services.schedule_service import ScheduleService

class ScheduleController:
    def __init__(self):
        self.service = ScheduleService()

    def get_student_schedule(self, student_id, semester):
        return self.service.get_student_schedule(student_id, semester).get_content()

    def add_calendar_decorator(self, student_id, semester, decorator_type):
        schedule = self.service.get_student_schedule(student_id, semester)
        decorated = self.service.add_calendar_decorator(schedule, decorator_type)
        return decorated.get_content()

    def generate_calendar(self, student_id, format_type):
        return self.service.generate_calendar(student_id, format_type)
