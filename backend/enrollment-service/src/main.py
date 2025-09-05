
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
