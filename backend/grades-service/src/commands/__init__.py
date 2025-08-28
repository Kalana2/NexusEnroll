from abc import ABC, abstractmethod


class gradeCommand(ABC):
    @abstractmethod
    def execute(self):
        pass
