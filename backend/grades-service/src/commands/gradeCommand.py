from abc import ABC, abstractmethod


class GradeCommand(ABC):
    @abstractmethod
    def execute(self):
        pass
