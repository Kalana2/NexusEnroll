import pandas as pd


class XLSXAdapter:
    def export(self, dataframe: pd.DataFrame, filename: str):
        file_path = f"{filename}.xlsx"
        dataframe.to_excel(file_path, index=False)
        return file_path
