# Serve signup page

from fastapi import FastAPI, Form, Response, Cookie, HTTPException
from .routes import gateway_routes
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI(title="NexusEnroll API Gateway")


# List of allowed origins (frontend URLs that can call this backend)
origins = [
    "http://localhost:5175",   # React, Vue, Angular dev server
    "http://127.0.0.1:5175",
    "*",  # Production frontend
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],  # no "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




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


from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(request: LoginRequest, response: Response):
    email = request.email
    password = request.password
    print(email, password)


    # Query Supabase for user with matching email
    result = supabase.table("users").select("*").eq("email", email).execute()
    users = result.data
        

    if not len(users):
        return {"success": False, "message": "Invalid email or password"}
    user = users[0]

    # response.set_cookie(key="userid" , value=user["id"] , httponly=False)
    # Check password (assuming plain text for demo; use hashed passwords in production)
    if user.get("password") == password:
        role = user.get("role", "user")
        role = user.get("role", "user")
        resp = JSONResponse(content={"success": True, "role": role})
        resp.set_cookie(key="userid", value=user["id"])
        response.set_cookie(key="userid" , value=user["id"])
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
async def student_page(userid : str = Cookie(None)):

    print({userid : userid})

    if not userid:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    result = supabase.table("users").select("*").eq("id", str(userid)).execute()


    user = result.data

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")


    user = user[0]

    with open("/app/frontend_student/student.html", "r") as f:
        html_content = f.read()


    html_content = html_content.replace("%%PROFILE_PHOTO%%" , user["photo"])
    html_content = html_content.replace("%%PROFILE_NAME%%" , user["name"])

    return html_content


# Serve faculty page
@app.get("/faculty", response_class=HTMLResponse)
async def faculty_page():
    with open("/app/frontend_faculty/faculty.html", "r") as f:
        html_content = f.read()
    return html_content


@app.get("/signup", response_class=HTMLResponse)
async def signup_page():
    with open("/app/frontend_login/signup.html", "r") as f:
        html_content = f.read()
    return html_content


# Handle signup form submission
@app.post("/signup", response_class=HTMLResponse)
async def signup(
    email: str = Form(...), password: str = Form(...), name: str = Form(...)
):
    # Create user in Supabase as student
    supabase.table("users").insert(
        {"email": email, "password": password, "name": name, "role": "student"}
    ).execute()
    with open("/app/frontend_student/student.html", "r") as f:
        html_content = f.read()
    return html_content


@app.get("/enroll")
async def redirect_to_enroll():
    return RedirectResponse(url="http://enrollment-service:8003/enroll")
