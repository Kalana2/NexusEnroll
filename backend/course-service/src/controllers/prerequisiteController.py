from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from ..services.prerequisiteService import PrerequisiteService
from ..models.course import Course

router = APIRouter(prefix="/prerequisites", tags=["prerequisites"])


def get_prerequisite_service():
    return PrerequisiteService()


@router.get(
    "/{course_id}", response_model=List[Course], summary="List course prerequisites"
)
async def list_prerequisites(
    course_id: str, service: PrerequisiteService = Depends(get_prerequisite_service)
):
    """
    List all prerequisites for a specific course.

    - **course_id**: The unique identifier of the course
    - Returns: List of prerequisite courses
    """
    try:
        prerequisites = service.list_prerequisites(course_id)
        if prerequisites is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found",
            )
        return prerequisites
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving prerequisites: {str(e)}",
        )


@router.post(
    "/{course_id}/{prerequisite_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add prerequisite",
)
async def add_prerequisite(
    course_id: str,
    prerequisite_id: str,
    service: PrerequisiteService = Depends(get_prerequisite_service),
):
    """
    Add a prerequisite to a course.

    - **course_id**: The unique identifier of the course
    - **prerequisite_id**: The unique identifier of the prerequisite course
    """
    try:
        success = service.add_prerequisite(course_id, prerequisite_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add prerequisite. Check if both courses exist.",
            )
        return {"message": "Prerequisite added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding prerequisite: {str(e)}",
        )


@router.delete(
    "/{course_id}/{prerequisite_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove prerequisite",
)
async def remove_prerequisite(
    course_id: str,
    prerequisite_id: str,
    service: PrerequisiteService = Depends(get_prerequisite_service),
):
    """
    Remove a prerequisite from a course.

    - **course_id**: The unique identifier of the course
    - **prerequisite_id**: The unique identifier of the prerequisite course to remove
    """
    try:
        success = service.remove_prerequisite(course_id, prerequisite_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove prerequisite. Check if the prerequisite exists.",
            )
        return {"message": "Prerequisite removed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing prerequisite: {str(e)}",
        )


@router.get(
    "/{course_id}/check/{prerequisite_id}", summary="Check if prerequisite exists"
)
async def check_prerequisite(
    course_id: str,
    prerequisite_id: str,
    service: PrerequisiteService = Depends(get_prerequisite_service),
):
    """
    Check if a specific course is a prerequisite for another course.

    - **course_id**: The unique identifier of the course
    - **prerequisite_id**: The unique identifier of the prerequisite course to check
    - Returns: Boolean indicating if the prerequisite exists
    """
    try:
        # This would typically be a method in the service
        # For now, we'll simulate the check
        prerequisites = service.list_prerequisites(course_id)
        if prerequisites is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found",
            )

        prerequisite_ids = [p.id for p in prerequisites]
        return {"is_prerequisite": prerequisite_id in prerequisite_ids}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking prerequisite: {str(e)}",
        )
