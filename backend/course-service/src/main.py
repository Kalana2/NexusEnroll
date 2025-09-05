from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional, Dict

from config import settings
from models.course import Course, CourseUpdate
from models.courseTrend import CourseTrend
from services.courseService import CourseService
from services.prerequisiteService import PrerequisiteService

app = FastAPI(title="Course Service", version="1.0.0")


# Dependency injection
def get_course_service():
    return CourseService()


def get_prerequisite_service():
    return PrerequisiteService()


@app.get("/")
async def root():
    return {"message": "Course Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Course endpoints
@app.get("/courses", response_model=List[Course])
async def browse_courses(
    keywords: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    instructor: Optional[str] = Query(None),
    service: CourseService = Depends(get_course_service),
):
    """Browse courses with optional filtering"""
    filters = {}
    if department:
        filters["department"] = department
    if instructor:
        filters["instructor"] = instructor

    return service.browse_courses(keywords, filters)


@app.get("/courses/{course_id}", response_model=Course)
async def get_course(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """Get a specific course by ID"""
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses/{course_id}/capacity")
async def get_course_capacity(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """Get capacity information for a course"""
    capacity = service.get_course_capacity(course_id)
    if not capacity:
        raise HTTPException(status_code=404, detail="Course not found")
    return capacity


@app.get("/courses/analytics/trending", response_model=List[CourseTrend])
async def get_courses_trending_data(
    service: CourseService = Depends(get_course_service),
):
    """Get trending course data"""
    return service.get_courses_trending_data()


@app.patch("/courses/{course_id}", response_model=Course)
async def update_course_info(
    course_id: str,
    updates: CourseUpdate,
    service: CourseService = Depends(get_course_service),
):
    """Update course information"""
    updated_course = service.update_course_info(
        course_id, updates.dict(exclude_unset=True)
    )
    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated_course


# Prerequisite endpoints
@app.get("/prerequisites/{course_id}", response_model=List[Course])
async def list_prerequisites(
    course_id: str, service: PrerequisiteService = Depends(get_prerequisite_service)
):
    """List all prerequisites for a course"""
    prerequisites = service.list_prerequisites(course_id)
    if prerequisites is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return prerequisites


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
