from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from pathlib import Path
from src.services.reporting_service import ReportingService
from src.services.clients import CourseServiceClient

# Dependency: create the service (would inject real base URLs in prod)
def get_service() -> ReportingService:
    client = CourseServiceClient()  # uses env COURSE_SERVICE_URL if set
    out_dir = os.getenv("OUT_DIR", "out")
    return ReportingService(course_client=client, out_dir=out_dir)

app = FastAPI(
    title="NexusEnroll Reporting Service",
    version="1.0.0",
    description="Exports admin reports (Adapter + Strategy + Facade)."
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/reports/capacity/export")
def export_capacity(
    dept: str = Query(..., description="Department name e.g. Business"),
    threshold: float = Query(..., ge=0, le=1, description="0.0 - 1.0 fill rate"),
    format: str = Query("csv", pattern="^(csv|xlsx|pdf)$"),
    filename: str = Query("capacity_report"),
    svc: ReportingService = Depends(get_service),
):
    """
    Example:
      /reports/capacity/export?dept=Business&threshold=0.9&format=csv&filename=biz_capacity
    """
    try:
        path = svc.export_capacity_report(dept, threshold, format, filename)
        media = {
            "csv": "text/csv",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "pdf": "application/pdf",
        }[format]
        return FileResponse(path=path, media_type=media, filename=Path(path).name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # never leak stack traces in prod; keep it simple here
        return JSONResponse(status_code=500, content={"error": str(e)})
