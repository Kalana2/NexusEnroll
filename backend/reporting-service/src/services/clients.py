"""
Service clients. In prod, call other services via HTTP.
For the POC we keep a stub dataset so this service runs standalone.
Swap the stub with real HTTP later (httpx client scaffold is included).
"""
from typing import List, Optional
from src.models import Course
import os

class CourseServiceClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("COURSE_SERVICE_URL")

    def list_courses(self, dept: str) -> List[Course]:
        if self.base_url:
            # --- Example of real HTTP call shape (uncomment when backend is ready) ---
            # import httpx
            # r = httpx.get(f"{self.base_url}/courses", params={"dept": dept}, timeout=10)
            # r.raise_for_status()
            # items = r.json()  # expecting list of dicts
            # return [Course(**it) for it in items]
            raise NotImplementedError("HTTP client path not wired in the POC.")
        # ------ Stub data so the service is runnable now ------
        data = [
            Course("CS101","Intro to CS","Business",100,93,"Dr. Perera"),
            Course("CS102","Data Structures","CS",180,160,"Dr. Silva"),
            Course("MKT210","Digital Marketing","Business",120,119,"Dr. Fernando"),
            Course("FIN300","Financial Analytics","Business",60,48,"Dr. Jayasena"),
        ]
        return [c for c in data if c.dept == dept]
