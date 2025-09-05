from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd


class PDFAdapter:
    def export(self, dataframe: pd.DataFrame, filename: str):
        file_path = f"{filename}.pdf"
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        text_object = c.beginText(50, height - 50)
        text_object.setFont("Helvetica", 10)

        # Write column headers
        text_object.textLine(" | ".join(dataframe.columns))

        # Write rows
        for _, row in dataframe.iterrows():
            text_object.textLine(" | ".join(str(x) for x in row.values))

        c.drawText(text_object)
        c.save()
        return file_path
