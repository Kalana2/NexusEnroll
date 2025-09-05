from dataclasses import dataclass


@dataclass
class BatchJob:
    job_id: str
    course_id: str
    status: str  # "submitted", "approved", "failed"
    record_count: int
