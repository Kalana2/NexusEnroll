from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from ..services.course_service import CourseService
from ..models.course import Course, CourseUpdate
from ..models.course_trend import CourseTrend

router = APIRouter()


def get_course_service():
    return CourseService()


@router.get("/", response_model=List[Course])
async def browse_courses(
    keywords: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    instructor: Optional[str] = Query(None),
    service: CourseService = Depends(get_course_service),
):
    """Browse courses with optional filtering"""
    filters = {}
    if keywords:
        filters["keywords"] = keywords
    if department:
        filters["department"] = department
    if instructor:
        filters["instructor"] = instructor

    return service.browse_courses(filters)


@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """Get a specific course by ID"""
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/capacity")
async def get_course_capacity(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """Get capacity information for a course"""
    capacity = service.get_course_capacity(course_id)
    if not capacity:
        raise HTTPException(status_code=404, detail="Course not found")
    return capacity


@router.get("/analytics/trending", response_model=List[CourseTrend])
async def get_courses_trending_data(
    service: CourseService = Depends(get_course_service),
):
    """Get trending course data"""
    return service.get_courses_trending_data()


@router.patch("/{course_id}", response_model=Course)
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
