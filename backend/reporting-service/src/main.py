from fastapi import FastAPI
from controllers import report_controller

app = FastAPI(title="Reporting Service")

app.include_router(report_controller.router, prefix="/reports", tags=["Reports"])


@app.get("/")
def root():
    return {"message": "Reporting Service is running"}
