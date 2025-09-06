from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Enrollment Service is running!"}


# Serve course enrollment form
@app.get("/enroll", response_class=HTMLResponse)
async def enroll_form():
    with open("/app/frontend_admin/courseform.html", "r") as f:
        html_content = f.read()
    return html_content


@app.get("/enrollment")
async def get_enrollment():
    return {
        "enrollment": [
            {
                "course": "CS 201 — Data Structures",
                "instructor": "Dr. Patel",
                "schedule": "Mon/Wed 09:00–11:00",
                "status": "Ready to Enroll",
            },
            {
                "course": "MATH 310 — Linear Algebra",
                "instructor": "Prof. Nguyen",
                "schedule": "Tue/Thu 13:00–15:00",
                "status": "Pending Validation",
            },
            {
                "course": "ENG 102 — Composition II",
                "instructor": "Dr. Chen",
                "schedule": "Fri 09:00–11:30",
                "status": "Time Conflict",
            },
        ]
    }
