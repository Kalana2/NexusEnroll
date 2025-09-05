from abc import ABC, abstractmethod

class ScheduleView(ABC):
    """Base interface for schedule view."""
    @abstractmethod
    def get_content(self):
        pass


class BaseSchedule(ScheduleView):
    """Basic schedule without decorations."""
    def __init__(self, schedule_data):
        self.schedule_data = schedule_data

    def get_content(self):
        return self.schedule_data


class ScheduleDecorator(ScheduleView):
    """Abstract decorator for schedules."""
    def __init__(self, schedule_view: ScheduleView):
        self._schedule_view = schedule_view

    @abstractmethod
    def get_content(self):
        pass
