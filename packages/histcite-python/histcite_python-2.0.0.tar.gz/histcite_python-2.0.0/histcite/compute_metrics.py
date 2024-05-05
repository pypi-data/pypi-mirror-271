"""This module is used to generate and export descriptive statistics."""

from pathlib import Path
from typing import Literal, Optional

import pandas as pd

wos_analyses_index = [
    "Records",
    "Authors",
    "Journals",
    "Keywords",
    "Yearly output",
    "Document Type",
    "Institution",
    "Institution with Subdivision",
    "Corresponding Authors",
    "Country",
]

cssci_analyses_index = [
    "Records",
    "Authors",
    "Journals",
    "Keywords",
    "Yearly output",
    "Institution",
]

scopus_analyses_index = [
    "Records",
    "Authors",
    "Journals",
    "Keywords",
    "Yearly output",
    "Document Type",
]


class ComputeMetrics:
    """Compute descriptive statistics of docs."""

    def __init__(
        self,
        docs_df: pd.DataFrame,
        citation_matrix: pd.DataFrame,
        source: Literal["wos", "cssci", "scopus"],
    ):
        self.merged_docs_df = docs_df.merge(citation_matrix[["node", "LCR", "LCS"]], on="node")
        self.source = source

    def check_sheets(self) -> list[str]:
        if self.source == "wos":
            return wos_analyses_index
        elif self.source == "cssci":
            return cssci_analyses_index
        elif self.source == "scopus":
            return scopus_analyses_index
        else:
            raise ValueError("Invalid source type")

    def generate_df_factory(
        self,
        use_cols: list[str],
        col: str,
        split_char: Optional[str] = None,
        lower_case: bool = False,
        sort_by_col: Literal["Recs", "TLCS", "TGCS"] = "Recs",
    ) -> pd.DataFrame:
        """A factory method to generate DataFrame of specific field.

        Args:
            use_cols: Columns to use. e.g. `["AU", "LCS", "TC"]`.
            col: Column to analyze. e.g. `AU`.
            split_char: Whether to split string. e.g. `; `. Default None.
            lower_case: Whether to convert string to lowercase. Default False.
            sort_by_col: Sort DataFrame by column. `Recs`, `TLCS` or `TGCS`. Default `Recs`.

        Returns:
            A DataFrame with some statitical metrics.
        """
        assert col in use_cols, "Argument <col> must be in <use_cols>"
        if sort_by_col == "TLCS":
            assert "LCS" in use_cols
        elif sort_by_col == "TGCS":
            assert "TC" in use_cols

        df = self.merged_docs_df[use_cols].dropna(subset=[col])
        if lower_case:
            df[col] = df[col].str.lower()
        if split_char:
            df[col] = df[col].str.split(split_char)
            df = df.explode(col, ignore_index=True)

        agg_dict = {col: "count"}
        if "LCS" in use_cols:
            agg_dict.update({"LCS": "sum"})
        if "TC" in use_cols:
            agg_dict.update({"TC": "sum"})
        grouped_df = df.groupby(col).agg(agg_dict)
        grouped_df.rename(columns={col: "Recs", "LCS": "TLCS", "TC": "TGCS"}, inplace=True)
        return grouped_df.sort_values(sort_by_col, ascending=False)

    def generate_record_df(self) -> pd.DataFrame:
        """Return record DataFrame."""
        use_cols = [
            "AU",
            "TI",
            "SO",
            "PY",
            "LCS",
            "TC",
            "LCR",
            "NR",
            "source file",
        ]
        if self.source == "cssci":
            use_cols.remove("TC")
        records_df = self.merged_docs_df[use_cols]
        if "TC" in use_cols:
            records_df = records_df.rename(columns={"TC": "GCS"})
        if "NR" in use_cols:
            records_df = records_df.rename(columns={"NR": "GCR"})
        return records_df

    def generate_author_df(self) -> pd.DataFrame:
        """Return author DataFrame."""
        use_cols = ["AU", "LCS", "TC"]
        if self.source == "cssci":
            use_cols.remove("TC")
        return self.generate_df_factory(use_cols, "AU", "; ")

    def generate_corresponding_author_df(self) -> pd.DataFrame:
        """Return corresponding author DataFrame. Only support WoS."""
        if self.source == "wos":
            use_cols = ["CAU", "LCS", "TC"]
        return self.generate_df_factory(use_cols, "CAU", "; ")

    def generate_keyword_df(self) -> pd.DataFrame:
        """Return keyword DataFrame."""
        use_cols = ["DE", "LCS", "TC"]
        if self.source == "cssci":
            use_cols.remove("TC")
        return self.generate_df_factory(use_cols, "DE", "; ", True)

    def generate_institution_df(self) -> pd.DataFrame:
        """Return institution DataFrame. Not support Scopus."""
        if self.source == "wos":
            use_cols = ["C3", "LCS", "TC"]
        elif self.source == "cssci":
            use_cols = ["C3", "LCS"]
        return self.generate_df_factory(use_cols, "C3", "; ")

    def generate_sub_institution_df(self) -> pd.DataFrame:
        """Return institution with subdivision DataFrame. Only support WoS."""
        if self.source == "wos":
            use_cols = ["I2", "LCS", "TC"]
        return self.generate_df_factory(use_cols, "I2", "; ")

    def generate_country_df(self) -> pd.DataFrame:
        """Return country DataFrame. Only support WoS."""
        if self.source == "wos":
            use_cols = ["CO", "LCS", "TC"]
        return self.generate_df_factory(use_cols, "CO", "; ")

    def generate_journal_df(self) -> pd.DataFrame:
        """Return journal DataFrame."""
        use_cols = ["SO", "LCS", "TC"]
        if self.source == "cssci":
            use_cols.remove("TC")
        return self.generate_df_factory(use_cols, "SO")

    def generate_year_df(self) -> pd.DataFrame:
        """Return publication year DataFrame."""
        use_cols = ["PY"]
        return self.generate_df_factory(use_cols, "PY").sort_values(by="PY")

    def generate_document_type_df(self) -> pd.DataFrame:
        """Return document type DataFrame. Not support CSSCI."""
        use_cols = ["DT"]
        return self.generate_df_factory(use_cols, "DT")

    def write2excel(self, save_path: Path):
        """Write all dataframes to an excel file. Each dataframe is a sheet.

        Args:
            save_path: The path to save the excel file. e.g. `.../descriptive_statistics.xlsx`

        Returns:
            An excel file with multiple sheets.
        """
        Path.mkdir(save_path.parent, exist_ok=True)
        with pd.ExcelWriter(save_path) as writer:
            self.generate_record_df().to_excel(writer, sheet_name="Records", index=False)
            self.generate_author_df().to_excel(writer, sheet_name="Authors")
            self.generate_journal_df().to_excel(writer, sheet_name="Journals")
            self.generate_keyword_df().to_excel(writer, sheet_name="Keywords")
            self.generate_year_df().to_excel(writer, sheet_name="Yearly output")

            if self.source == "wos":
                self.generate_document_type_df().to_excel(writer, sheet_name="Document Type")
                self.generate_institution_df().to_excel(writer, sheet_name="Institution")
                self.generate_sub_institution_df().to_excel(writer, sheet_name="Institution with Subdivision")
                self.generate_country_df().to_excel(writer, sheet_name="Country")
                self.generate_corresponding_author_df().to_excel(writer, sheet_name="Corresponding Authors")

            elif self.source == "scopus":
                self.generate_document_type_df().to_excel(writer, sheet_name="Document Type")

            elif self.source == "cssci":
                self.generate_institution_df().to_excel(writer, sheet_name="Institution")
