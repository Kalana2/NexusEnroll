from adapters.csv_adapter import CSVAdapter
from adapters.xlsx_adapter import XLSXAdapter
from adapters.pdf_adapter import PDFAdapter
import pandas as pd


class ReportService:
    def __init__(self):
        self.adapters = {
            "CSV": CSVAdapter(),
            "XLSX": XLSXAdapter(),
            "PDF": PDFAdapter(),
        }

    def generate_report(self, report_type: str, format: str):
        # Dummy data for now
        data = pd.DataFrame(
            [
                {"course": "CS101", "students": 120, "faculty": "Dr. Smith"},
                {"course": "MATH201", "students": 80, "faculty": "Dr. Doe"},
            ]
        )

        adapter = self.adapters.get(format)
        if not adapter:
            raise ValueError("Unsupported format")

        file_path = adapter.export(data, f"{report_type}_report")
        return {"status": "success", "file": file_path}
