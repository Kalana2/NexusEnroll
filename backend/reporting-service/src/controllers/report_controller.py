from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from src.services.reporting_service import ReportingService

app = FastAPI(title="Reporting Service", version="1.0.0")
svc = ReportingService()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/reports/capacity/export")
def export_capacity(
    dept: str = Query(..., description="Department name"),
    threshold: float = Query(..., ge=0, le=1, description="0.0 - 1.0"),
    format: str = Query("csv", regex="^(csv|xlsx|pdf)$"),
    filename: str = Query("capacity_report"),
):
    """
    Example:
    /reports/capacity/export?dept=Business&threshold=0.9&format=csv&filename=biz_capacity
    """
    try:
        path = svc.export_capacity_report(dept, threshold, format, filename)
        if format == "csv":
            media = "text/csv"
        elif format == "xlsx":
            media = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            media = "application/pdf"
        return FileResponse(path=path, media_type=media, filename=path.split("/")[-1])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
