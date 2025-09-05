from dataclasses import dataclass
from supabase import Client, create_client


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "batch_jobs"


@dataclass
class BatchJob:
    job_id: str
    course_id: str
    status: str  # "submitted", "approved", "failed"
    record_count: int


def _table():
    return supabase.table(TABLE_NAME)


def create_batch_job(job_id: str, course_id: str, status: str, record_count: int):
    """Insert a new batch job record."""
    payload = {
        "job_id": job_id,
        "course_id": course_id,
        "status": status,
        "record_count": record_count,
    }
    res = _table().insert(payload).execute()
    return res.data


def fetch_batch_job(job_id: str):
    """Fetch a single batch job by job_id."""
    res = _table().select("*").eq("job_id", job_id).single().execute()
    return res.data


def update_batch_job_status(job_id: str, status: str):
    """Update status field of a batch job."""
    res = _table().update({"status": status}).eq("job_id", job_id).execute()
    return res.data


def list_jobs_by_course(course_id: str):
    """List all batch jobs for a given course_id."""
    res = _table().select("*").eq("course_id", course_id).execute()
    return res.data
