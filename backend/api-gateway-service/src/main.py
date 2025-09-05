from fastapi import FastAPI, Form
from .routes import gateway_routes
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client






SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="NexusEnroll API Gateway")



# Mount static files from /app/public at /static
app.mount("/static", StaticFiles(directory="/app/public"), name="static")

# Include gateway routes
app.include_router(gateway_routes.router)



# Serve login page at root
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("/app/frontend_login/login.html", "r") as f:
        html_content = f.read()
    return html_content

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):

    print(email , password)
    # Query Supabase for user with matching email
    result = supabase.table("users").select("*").eq("email", email).execute()
    users = result.data
    
    print("users :" , users)
    if not len(users):
        return {"success": False, "message": "Invalid email or password"}
    user = users[0]
    # Check password (assuming plain text for demo; use hashed passwords in production)
    if user.get("password") == password:
        role = user.get("role", "user")
        return {"success": True, "role":role }
    else:
        return {"success": False, "message": "Invalid email or password"}
    

# Serve admin page
@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    with open("/app/frontend_admin/admin.html", "r") as f:
        html_content = f.read()
    return html_content

# Serve student page
@app.get("/student", response_class=HTMLResponse)
async def student_page():
    with open("/app/frontend_student/student.html", "r") as f:
        html_content = f.read()
    return html_content

# Serve faculty page
@app.get("/faculty", response_class=HTMLResponse)
async def faculty_page():
    with open("/app/frontend_faculty/faculty.html", "r") as f:
        html_content = f.read()
    return html_content