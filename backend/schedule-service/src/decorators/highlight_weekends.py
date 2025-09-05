from .base_decorator import ScheduleDecorator

class HighlightWeekendsDecorator(ScheduleDecorator):
    """Adds weekend highlighting."""
    def get_content(self):
        schedule = self._schedule_view.get_content()
        for day in schedule:
            if day["day"] in ["Saturday", "Sunday"]:
                day["highlight"] = "Weekend"
        return schedule
