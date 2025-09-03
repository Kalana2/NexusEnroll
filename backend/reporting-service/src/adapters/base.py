from typing import Protocol, Sequence, Mapping

class Exporter(Protocol):
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        ...
