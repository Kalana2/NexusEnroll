class ThirdPartyXlsxWriter:
    def write_sheet(self, sheet_name: str, headers, data, path: str):
        # For demo we write a simple TSV with .xlsx extension.
        if not path.endswith(".xlsx"):
            path += ".xlsx"
        with open(path, "w", encoding="utf-8") as f:
            f.write("\t".join(headers) + "\n")
            for row in data:
                f.write("\t".join(str(row[h]) for h in headers) + "\n")
        return path
