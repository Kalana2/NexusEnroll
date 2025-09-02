# ========== common/dtos.py ==========
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Course:
    id: str
    name: str
    dept: str
    capacity: int
    enrolled: int
    instructor: str

# ========== api_gateway/auth.py ==========
# (Proxy + simple token/RBAC utilities; in prod you'd use JWT/OAuth2)
import hmac, hashlib, json, base64
SECRET = b"demo-secret"

def sign(payload: dict) -> str:
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    sig = hmac.new(SECRET, data, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(data + b"." + sig).decode()

def verify(token: str) -> dict:
    raw = base64.urlsafe_b64decode(token.encode())
    data, sig = raw.rsplit(b".", 1)
    if hmac.compare_digest(hmac.new(SECRET, data, hashlib.sha256).digest(), sig):
        return json.loads(data.decode())
    raise ValueError("Invalid token")

# ========== api_gateway/middlewares.py ==========
# Chain of Responsibility: Auth -> RBAC -> Input Validation
from typing import Callable, Any, Dict

Handler = Callable[[Dict[str, Any]], Any]

def auth_middleware(next_handler: Handler) -> Handler:
    def _h(req):
        from .auth import verify
        req["user"] = verify(req["token"])  # raises if invalid
        return next_handler(req)
    return _h

def rbac_middleware(allowed_roles: set):
    def wrap(next_handler: Handler) -> Handler:
        def _h(req):
            role = req["user"]["role"]
            if role not in allowed_roles:
                raise PermissionError(f"Role {role} not permitted")
            return next_handler(req)
        return _h
    return wrap

def validate_params(required: set):
    def wrap(next_handler: Handler) -> Handler:
        def _h(req):
            missing = [k for k in required if k not in req.get("query", {})]
            if missing:
                raise ValueError(f"Missing params: {missing}")
            return next_handler(req)
        return _h
    return wrap

# ========== api_gateway/clients.py ==========
# Lightweight service clients (stubs). In real system these call HTTP.
from typing import List
from common.dtos import Course

class CourseServiceClient:
    def list_courses(self, dept: str) -> List[Course]:
        # demo dataset
        data = [
            Course("CS101","Intro to CS","Business",100,93,"Dr. Perera"),
            Course("CS102","Data Structures","CS",180,160,"Dr. Silva"),
            Course("MKT210","Digital Marketing","Business",120,119,"Dr. Fernando"),
            Course("FIN300","Financial Analytics","Business",60,48,"Dr. Jayasena"),
        ]
        return [c for c in data if c.dept == dept]

class EnrollmentServiceClient:
    # kept for future aggregation; not needed for this specific report
    def current_enrollment(self, course_id: str) -> int:
        return 0

# ========== reporting_service/exporters/base.py ==========
from typing import Protocol, Sequence, Mapping

class Exporter(Protocol):
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        """Write rows to filename, return path."""

# ========== reporting_service/exporters/csv_exporter.py ==========
import csv
from typing import Sequence, Mapping

class CsvExporter:
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        if not filename.endswith(".csv"):
            filename += ".csv"
        if not rows:
            open(filename, "w").close()
            return filename
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        return filename

# ========== reporting_service/exporters/xlsx_thirdparty.py ==========
# Pretend third-party API with a different interface (so we need an Adapter).
class ThirdPartyXlsxWriter:
    def write_sheet(self, sheet_name: str, headers, data, path: str):
        # For the POC we just write a TSV; team can swap in openpyxl later.
        if not path.endswith(".xlsx"): path += ".xlsx"
        with open(path, "w", encoding="utf-8") as f:
            f.write("\t".join(headers) + "\n")
            for row in data:
                f.write("\t".join(str(row[h]) for h in headers) + "\n")
        return path

# ========== reporting_service/exporters/xlsx_adapter.py ==========
from typing import Sequence, Mapping
from .base import Exporter
from .xlsx_thirdparty import ThirdPartyXlsxWriter

class XlsxExporterAdapter(Exporter):
    """Adapter: adapts ThirdPartyXlsxWriter to our Exporter interface."""
    def __init__(self):
        self._lib = ThirdPartyXlsxWriter()
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        headers = list(rows[0].keys()) if rows else []
        return self._lib.write_sheet("report", headers, rows, filename)

# ========== reporting_service/exporters/pdf_thirdparty.py ==========
class ThirdPartyPdfLib:
    def render_table(self, title: str, rows, path: str):
        if not path.endswith(".pdf"): path += ".pdf"
        # Minimal placeholder: write plain text (swap with reportlab later)
        with open(path, "w", encoding="utf-8") as f:
            f.write(title + "\n\n")
            if rows:
                f.write(" | ".join(rows[0].keys()) + "\n")
                for r in rows:
                    f.write(" | ".join(str(v) for v in r.values()) + "\n")
        return path

# ========== reporting_service/exporters/pdf_adapter.py ==========
from typing import Sequence, Mapping
from .base import Exporter
from .pdf_thirdparty import ThirdPartyPdfLib

class PdfExporterAdapter(Exporter):
    """Adapter to unify ThirdPartyPdfLib to Exporter."""
    def __init__(self):
        self._lib = ThirdPartyPdfLib()
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        return self._lib.render_table("NexusEnroll Report", rows, filename)

# ========== reporting_service/service.py ==========
# Facade + Strategy: one simple API that hides exporters & data fetching
from typing import List, Dict
from common.dtos import Course
from .exporters.csv_exporter import CsvExporter
from .exporters.xlsx_adapter import XlsxExporterAdapter
from .exporters.pdf_adapter import PdfExporterAdapter

class ReportingService:
    def __init__(self, course_client):
        self.course_client = course_client
        # Strategy map for format -> exporter
        self.export_strategies = {
            "csv": CsvExporter(),
            "xlsx": XlsxExporterAdapter(),   # Adapter in action
            "pdf": PdfExporterAdapter(),     # Adapter in action
        }

    def courses_over_capacity(
        self, dept: str, threshold: float
    ) -> List[Dict]:
        """Return rows of courses with enrolled/capacity >= threshold."""
        courses: List[Course] = self.course_client.list_courses(dept)
        rows = []
        for c in courses:
            fill = c.enrolled / max(c.capacity, 1)
            if fill >= threshold:
                rows.append({
                    "course_id": c.id,
                    "name": c.name,
                    "dept": c.dept,
                    "capacity": c.capacity,
                    "enrolled": c.enrolled,
                    "fill_rate": f"{fill:.0%}",
                    "instructor": c.instructor
                })
        return rows

    def export_capacity_report(
        self, dept: str, threshold: float, fmt: str, filename: str
    ) -> str:
        rows = self.courses_over_capacity(dept, threshold)
        exporter = self.export_strategies.get(fmt.lower())
        if not exporter:
            raise ValueError(f"Unsupported format: {fmt}")
        return exporter.export(rows, filename)

# ========== api_gateway/gateway.py ==========
# Proxy + Aggregation endpoint that calls Reporting Facade
from typing import Dict, Any
from .middlewares import auth_middleware, rbac_middleware, validate_params
from .clients import CourseServiceClient
from reporting_service.service import ReportingService

class ApiGateway:
    def __init__(self):
        self.course_client = CourseServiceClient()
        self.reporting = ReportingService(self.course_client)

    # ------------ Route: GET /reports/capacity  (Admin-only) ------------
    def handle_report_capacity(self, req: Dict[str, Any]) -> Dict[str, Any]:
        def core(r):
            q = r["query"]
            path = self.reporting.export_capacity_report(
                dept=q["dept"], threshold=float(q["threshold"]),
                fmt=q.get("format","csv"), filename=q.get("filename","capacity_report")
            )
            return {"status": 200, "path": path}

        # Chain of Responsibility pipeline:
        handler = auth_middleware(
                    rbac_middleware({"admin"})(   # only admins
                        validate_params({"dept","threshold"})(core)
                    )
                 )
        return handler(req)

# ========== main_demo.py ==========
from api_gateway.gateway import ApiGateway
from api_gateway.auth import sign

if __name__ == "__main__":
    # Create an ADMIN token (other teams can create student/faculty similarly)
    token = sign({"user_id":"A-100","role":"admin"})
    gw = ApiGateway()

    # Admin asks for Business school courses >90% capacity, export to CSV
    req = {
        "token": token,
        "query": {"dept":"Business","threshold":"0.9","format":"csv","filename":"biz_capacity"}
    }
    resp = gw.handle_report_capacity(req)
    print("Response:", resp)
    # -> {'status': 200, 'path': 'biz_capacity.csv'}
