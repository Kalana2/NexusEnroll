import csv
from typing import Sequence, Mapping

class CsvExporter:
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        if not filename.endswith(".csv"):
            filename += ".csv"
        if not rows:
            open(filename, "w").close()
            return filename
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        return filename
