from typing import List, Dict
from src.models import Course
from src.services.clients import CourseServiceClient
from src.adapters.csv_exporter import CsvExporter
from src.adapters.xlsx_adapter import XlsxExporterAdapter
from src.adapters.pdf_adapter import PdfExporterAdapter

class ReportingService:
    def __init__(self, course_client: CourseServiceClient | None = None):
        self.course_client = course_client or CourseServiceClient()
        self.export_strategies = {
            "csv": CsvExporter(),
            "xlsx": XlsxExporterAdapter(),   # Adapter in action
            "pdf": PdfExporterAdapter(),     # Adapter in action
        }

    def courses_over_capacity(self, dept: str, threshold: float) -> List[Dict]:
        courses: List[Course] = self.course_client.list_courses(dept)
        rows: List[Dict] = []
        for c in courses:
            fill = c.enrolled / max(c.capacity, 1)
            if fill >= threshold:
                rows.append({
                    "course_id": c.id,
                    "name": c.name,
                    "dept": c.dept,
                    "capacity": c.capacity,
                    "enrolled": c.enrolled,
                    "fill_rate": f"{fill:.0%}",
                    "instructor": c.instructor
                })
        return rows

    def export_capacity_report(self, dept: str, threshold: float,
                               fmt: str, filename: str) -> str:
        rows = self.courses_over_capacity(dept, threshold)
        exporter = self.export_strategies.get(fmt.lower())
        if not exporter:
            raise ValueError(f"Unsupported format: {fmt}")
        return exporter.export(rows, filename)
