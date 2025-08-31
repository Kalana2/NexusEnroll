from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional, Dict
from services.courseService import CourseService
from models.course import Course, CourseUpdate
from models.courseTrend import CourseTrend

router = APIRouter(prefix="/courses", tags=["courses"])


def get_course_service():
    return CourseService()


@router.get("/", response_model=List[Course], summary="Browse courses")
async def browse_courses(
    keywords: Optional[str] = Query(None, description="Search keywords"),
    department: Optional[str] = Query(None, description="Filter by department"),
    instructor: Optional[str] = Query(None, description="Filter by instructor"),
    service: CourseService = Depends(get_course_service),
):
    """
    Browse courses with optional filtering and search.

    - **keywords**: Search in course name, description, department, or instructor
    - **department**: Filter by department name
    - **instructor**: Filter by instructor name
    """
    try:
        filters = {}
        if department:
            filters["department"] = department
        if instructor:
            filters["instructor"] = instructor

        courses = service.browse_courses(keywords, filters)
        return courses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error browsing courses: {str(e)}",
        )


@router.get("/{course_id}", response_model=Course, summary="Get course by ID")
async def get_course(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """
    Get a specific course by its ID.

    - **course_id**: The unique identifier of the course
    """
    try:
        course = service.get_course(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found",
            )
        return course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving course: {str(e)}",
        )


@router.get("/{course_id}/capacity", summary="Get course capacity")
async def get_course_capacity(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """
    Get capacity information for a specific course.

    - **course_id**: The unique identifier of the course
    - Returns: Object with total capacity, remaining seats, and current enrollment
    """
    try:
        capacity = service.get_course_capacity(course_id)
        if not capacity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found",
            )
        return capacity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving course capacity: {str(e)}",
        )


@router.get(
    "/analytics/trending",
    response_model=List[CourseTrend],
    summary="Get trending courses",
)
async def get_courses_trending_data(
    service: CourseService = Depends(get_course_service),
):
    """
    Get trending course data with popularity scores and enrollment rates.

    - Returns: List of course trends with analytics data
    """
    try:
        return service.get_courses_trending_data()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving trending data: {str(e)}",
        )


@router.patch(
    "/{course_id}", response_model=Course, summary="Update course information"
)
async def update_course_info(
    course_id: str,
    updates: CourseUpdate,
    service: CourseService = Depends(get_course_service),
):
    """
    Update course information.

    - **course_id**: The unique identifier of the course to update
    - **updates**: Fields to update (partial update supported)
    """
    try:
        updated_course = service.update_course_info(
            course_id, updates.dict(exclude_unset=True)
        )
        if not updated_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found",
            )
        return updated_course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating course: {str(e)}",
        )


@router.post(
    "/",
    response_model=Course,
    status_code=status.HTTP_201_CREATED,
    summary="Create new course",
)
async def create_course(
    course: Course, service: CourseService = Depends(get_course_service)
):
    """
    Create a new course.

    - **course**: Course data to create
    """
    try:
        # In a real implementation, this would call a create method in the service
        # For now, we'll simulate creation by returning the input course
        # service.create_course(course)
        return course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating course: {str(e)}",
        )


@router.delete(
    "/{course_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete course"
)
async def delete_course(
    course_id: str, service: CourseService = Depends(get_course_service)
):
    """
    Delete a course by ID.

    - **course_id**: The unique identifier of the course to delete
    """
    try:
        # In a real implementation, this would call a delete method in the service
        # service.delete_course(course_id)
        return
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course: {str(e)}",
        )
