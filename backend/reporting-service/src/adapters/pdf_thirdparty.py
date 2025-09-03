class ThirdPartyPdfLib:
    def render_table(self, title: str, rows, path: str):
        if not path.endswith(".pdf"):
            path += ".pdf"
        with open(path, "w", encoding="utf-8") as f:
            f.write(title + "\n\n")
            if rows:
                f.write(" | ".join(rows[0].keys()) + "\n")
                for r in rows:
                    f.write(" | ".join(str(v) for v in r.values()) + "\n")
        return path
