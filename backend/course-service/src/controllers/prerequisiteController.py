from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..services.prerequisite_service import PrerequisiteService
from ..models.course import Course

router = APIRouter()


def get_prerequisite_service():
    return PrerequisiteService()


@router.get("/{course_id}", response_model=List[Course])
async def list_prerequisites(
    course_id: str, service: PrerequisiteService = Depends(get_prerequisite_service)
):
    """List all prerequisites for a course"""
    prerequisites = service.list_prerequisites(course_id)
    if prerequisites is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return prerequisites


@router.post("/{course_id}/{prerequisite_id}")
async def add_prerequisite(
    course_id: str,
    prerequisite_id: str,
    service: PrerequisiteService = Depends(get_prerequisite_service),
):
    """Add a prerequisite to a course"""
    success = service.add_prerequisite(course_id, prerequisite_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add prerequisite")
    return {"message": "Prerequisite added successfully"}


@router.delete("/{course_id}/{prerequisite_id}")
async def remove_prerequisite(
    course_id: str,
    prerequisite_id: str,
    service: PrerequisiteService = Depends(get_prerequisite_service),
):
    """Remove a prerequisite from a course"""
    success = service.remove_prerequisite(course_id, prerequisite_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove prerequisite")
    return {"message": "Prerequisite removed successfully"}
