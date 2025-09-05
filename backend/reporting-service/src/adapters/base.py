from typing import Protocol, Sequence, Mapping

class Exporter(Protocol):
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        """Write rows to a file and return the filesystem path."""
