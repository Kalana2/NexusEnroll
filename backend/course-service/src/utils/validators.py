from typing import List


def validate_course_data(course_data: dict) -> List[str]:
    """Validate course data and return list of errors"""
    errors = []

    # Check required fields
    required_fields = [
        "id",
        "name",
        "description",
        "department",
        "instructor",
        "credits",
        "total_capacity",
    ]
    for field in required_fields:
        if field not in course_data or not course_data[field]:
            errors.append(f"Missing required field: {field}")

    # Validate numeric fields
    if "credits" in course_data and not isinstance(course_data["credits"], int):
        errors.append("Credits must be an integer")

    if "total_capacity" in course_data and not isinstance(
        course_data["total_capacity"], int
    ):
        errors.append("Total capacity must be an integer")

    if "current_enrollment" in course_data and not isinstance(
        course_data["current_enrollment"], int
    ):
        errors.append("Current enrollment must be an integer")

    return errors
