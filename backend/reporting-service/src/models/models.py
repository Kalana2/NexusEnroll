from pydantic import BaseModel


class ReportRequest(BaseModel):
    report_type: str
    format: str
