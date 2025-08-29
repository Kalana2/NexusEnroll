class GradeService:

    VALID_GRADES = {"A", "B", "C", "D", "F"}

    def __init__(self):
        self.grades = {}
        self.pending = {}

    def submitGrades(self, courseId, gradeBatch):
        accepted = []
        rejected = []

        for record in gradeBatch:
            studentId, grade = record["studentId"], record["grade"]

            if not studentId or not grade:
                rejected.append({**record, "error": "Missing studentId or grade"})
                continue
            if grade not in self.VALID_GRADES:
                rejected.append({**record, "error": f"Invalid grade {grade}"})
                continue

            self.pending.setdefault(courseId, []).append(record)
            accepted.append(record)

        status = "success" if not rejected else ("partial" if accepted else "failed")
        return {
            "status": status,
            "courseId": courseId,
            "accepted": accepted,
            "rejected": rejected,
        }

    def approveGrades(self, course_id):
        if course_id not in self.pending:
            return {"status": "error", "message": "No pending grades"}

        batch = self.pending.pop(course_id)
        for record in batch:
            sid, grade = record["studentId"], record["grade"]
            self.grades.setdefault(sid, []).append(
                {"courseId": course_id, "grade": grade}
            )

        return {"status": "approved", "courseId": course_id, "count": len(batch)}

    def getGrades(self, student_id):
        return self.grades.get(student_id, [])
