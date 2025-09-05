import os
from fastapi import APIRouter, Request
from src.utils.proxy import proxy_request

router = APIRouter()


router = APIRouter()

# Service URLs from environment variables (docker-compose sets these)
USER_SERVICE = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
COURSE_SERVICE = os.getenv("COURSE_SERVICE_URL", "http://course-service:8002")
ENROLLMENT_SERVICE = os.getenv(
    "ENROLLMENT_SERVICE_URL", "http://enrollment-service:8003"
)
GRADES_SERVICE = os.getenv("GRADES_SERVICE_URL", "http://grades-service:8004")
REPORTING_SERVICE = os.getenv("REPORTING_SERVICE_URL", "http://reporting-service:8005")
SCHEDULE_SERVICE = os.getenv("SCHEDULE_SERVICE_URL", "http://schedule-service:8006")
NOTIFICATION_SERVICE = os.getenv(
    "NOTIFICATION_SERVICE_URL", "http://notification-service:8007"
)


# User Service
@router.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def users_proxy(path: str, request: Request):
    return await proxy_request(request, f"{USER_SERVICE}/{path}")


# Course Service
@router.api_route("/courses/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def courses_proxy(path: str, request: Request):
    return await proxy_request(request, f"{COURSE_SERVICE}/{path}")


# Enrollment Service
@router.api_route("/enrollments/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def enrollments_proxy(path: str, request: Request):
    return await proxy_request(request, f"{ENROLLMENT_SERVICE}/{path}")


# Grades Service
@router.api_route("/grades/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def grades_proxy(path: str, request: Request):
    return await proxy_request(request, f"{GRADES_SERVICE}/{path}")


# Reporting Service
@router.api_route("/reports/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def reports_proxy(path: str, request: Request):
    return await proxy_request(request, f"{REPORTING_SERVICE}/{path}")


# Schedule Service
@router.api_route("/schedule/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def schedule_proxy(path: str, request: Request):
    return await proxy_request(request, f"{SCHEDULE_SERVICE}/{path}")


# Notification Service
@router.api_route(
    "/notifications/{path:path}", methods=["GET", "POST", "PUT", "DELETE"]
)
async def notifications_proxy(path: str, request: Request):
    return await proxy_request(request, f"{NOTIFICATION_SERVICE}/{path}")
