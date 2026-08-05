"""
============================================================
Universal CSV Reader
============================================================

Responsibilities

• Load input and output CSV files
• Validate datasets
• Handle missing values
• Ensure both datasets are compatible

This module performs NO preprocessing.
============================================================
"""

import os
import pandas as pd


class CSVReader:

    def __init__(self, input_csv, output_csv):

        self.input_csv = input_csv
        self.output_csv = output_csv

    # ---------------------------------------------------------

    def load(self):
        import os

        print("\nLoading datasets...\n")

        print("Input CSV :", self.input_csv)
        print("Exists :", os.path.exists(self.input_csv))
        print("Size :", os.path.getsize(self.input_csv))


        self._validate_paths()

        input_df = pd.read_csv(self.input_csv)
        output_df = pd.read_csv(self.output_csv)

        input_df = self._clean(input_df)
        output_df = self._clean(output_df)

        self._validate_shape(input_df, output_df)

        print("=" * 60)
        print("CSV LOADING COMPLETED")
        print("=" * 60)

        print(f"Input File  : {self.input_csv}")
        print(f"Output File : {self.output_csv}")

        print()

        print("Input Examples :", len(input_df))
        print("Output Examples:", len(output_df))

        print()

        print("Input Columns")
        print(list(input_df.columns))

        print()

        print("Output Columns")
        print(list(output_df.columns))

        print("=" * 60)

        return input_df, output_df

    # ---------------------------------------------------------

    def _validate_paths(self):

        if not os.path.exists(self.input_csv):
            raise FileNotFoundError(
                f"Input CSV not found:\n{self.input_csv}"
            )

        if not os.path.exists(self.output_csv):
            raise FileNotFoundError(
                f"Output CSV not found:\n{self.output_csv}"
            )

    # ---------------------------------------------------------

    def _clean(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna("", inplace=True)

        dataframe.columns = [

            str(col).strip()

            for col in dataframe.columns

        ]

        return dataframe

    # ---------------------------------------------------------

    def _validate_shape(self, input_df, output_df):

        if len(input_df) != len(output_df):

            raise ValueError(

                "\nInput CSV and Output CSV contain "
                "different numbers of examples."

            )

        if len(input_df) == 0:

            raise ValueError(

                "\nDataset is empty."

            )

    # ---------------------------------------------------------

    def preview(self, dataframe, rows=5):

        print()

        print(dataframe.head(rows))