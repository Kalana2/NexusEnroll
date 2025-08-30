from .gradeCommand import GradeCommand


class ApprovalResult:
    def __init__(
        self, success: bool, course_id: str, count: int = 0, message: str = ""
    ):
        self.success = success
        self.course_id = course_id
        self.count = count
        self.message = message

    def to_dict(self):
        return {
            "success": self.success,
            "courseId": self.course_id,
            "count": self.count,
            "message": self.message,
        }


class ApproveGradesCommand(GradeCommand):
    def __init__(self, grade_service, course_id: str):
        self.grade_service = grade_service
        self.course_id = course_id

    def execute(self) -> ApprovalResult:
        result = self.grade_service.approveGrades(self.course_id)

        if result.get("status") == "approved":
            return ApprovalResult(
                True,
                self.course_id,
                count=result.get("count", 0),
                message=f"Grades for course {self.course_id} approved successfully",
            )
        else:
            return ApprovalResult(
                False,
                self.course_id,
                count=0,
                message=result.get("message", "Failed to approve grades"),
            )
