from typing import Sequence, Mapping
from .base import Exporter
from .pdf_thirdparty import ThirdPartyPdfLib

class PdfExporterAdapter(Exporter):
    """Adapter → unify ThirdPartyPdfLib to Exporter interface."""
    def __init__(self):
        self._lib = ThirdPartyPdfLib()
    def export(self, rows: Sequence[Mapping], filename: str) -> str:
        return self._lib.render_table("NexusEnroll Report", rows, filename)
