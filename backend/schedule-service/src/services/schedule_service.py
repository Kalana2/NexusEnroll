from src.decorators.base_decorator import BaseSchedule
from src.decorators.highlight_weekends import HighlightWeekendsDecorator
from src.decorators.add_holidays import AddHolidaysDecorator

class ScheduleService:
    """Handles schedule building and decoration."""

    def get_student_schedule(self, student_id, semester):
       # want to replace with kalana return values
        return BaseSchedule([
            {"day": "Monday", "date": "2025-09-01", "classes": ["Math", "Physics"]},
            {"day": "Saturday", "date": "2025-09-06", "classes": ["Sports"]},
            {"day": "Sunday", "date": "2025-09-07", "classes": []}
        ])

    def add_calendar_decorator(self, schedule_view, decorator_type):
        if decorator_type == "highlight_weekends":
            return HighlightWeekendsDecorator(schedule_view)
        elif decorator_type == "add_holidays":
            return AddHolidaysDecorator(schedule_view, holidays=["2025-09-06"])
        return schedule_view

    def generate_calendar(self, student_id, format_type="Weekly"):
        schedule = self.get_student_schedule(student_id, "2025-Fall")
        schedule = HighlightWeekendsDecorator(schedule)
        schedule = AddHolidaysDecorator(schedule, holidays=["2025-09-06"])
        return {
            "format": format_type,
            "data": schedule.get_content()
        }
