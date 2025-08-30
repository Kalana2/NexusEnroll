from abc import ABC, abstractmethod
from typing import Any


class GradeCommand(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass
