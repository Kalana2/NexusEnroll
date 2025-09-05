from fastapi import APIRouter, Query
from services.report_service import ReportService

router = APIRouter()
service = ReportService()


@router.get("/enrollment")
def generate_enrollment_report(format: str = Query("CSV", enum=["CSV", "XLSX", "PDF"])):
    return service.generate_report("enrollment", format)


@router.get("/faculty-workload")
def generate_faculty_report(format: str = Query("CSV", enum=["CSV", "XLSX", "PDF"])):
    return service.generate_report("faculty_workload", format)


@router.get("/course-popularity")
def generate_course_report(format: str = Query("CSV", enum=["CSV", "XLSX", "PDF"])):
    return service.generate_report("course_popularity", format)
