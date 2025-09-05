from typing import Sequence, Mapping
from .base import Exporter
from .xlsx_thirdparty import ThirdPartyXlsxWriter

class XlsxExporterAdapter(Exporter):
    """Adapts ThirdPartyXlsxWriter to our Exporter interface."""
    def __init__(self):
        self._lib = ThirdPartyXlsxWriter()
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        headers = list(rows[0].keys()) if rows else []
        return self._lib.write_sheet("report", headers, rows, filename)
