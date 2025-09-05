from .base_decorator import ScheduleDecorator

class AddHolidaysDecorator(ScheduleDecorator):
    """Adds holiday marking."""
    def __init__(self, schedule_view, holidays):
        super().__init__(schedule_view)
        self.holidays = holidays

    def get_content(self):
        schedule = self._schedule_view.get_content()
        for day in schedule:
            if day["date"] in self.holidays:
                day["holiday"] = "Holiday"
        return schedule
