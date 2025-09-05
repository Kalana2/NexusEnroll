import pandas as pd


class CSVAdapter:
    def export(self, dataframe: pd.DataFrame, filename: str):
        file_path = f"{filename}.csv"
        dataframe.to_csv(file_path, index=False)
        return file_path
