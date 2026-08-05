"""
============================================================
Unknown Black Box
============================================================

The black box NEVER contains any algorithm.

It simply observes examples.

============================================================
"""

from parser.csv_reader import CSVReader
from parser.parser import DatasetParser
from blackbox.observer import BlackBoxObserver


class UnknownBlackBox:

    def __init__(self, input_csv, output_csv):

        self.reader = CSVReader(
            input_csv,
            output_csv
        )

        self.parser = DatasetParser()

        self.observer = BlackBoxObserver()

    # -----------------------------------------------------

    def observe(self):

        print("\nObserving Unknown Black Box...\n")

        input_df, output_df = self.reader.load()

        dataset = self.parser.parse(
            input_df,
            output_df
        )

        observations = []

        for example in dataset:

            info = self.observer.observe(
                example.input_data,
                example.output_data
            )

            observations.append(info)

        self.print_summary(observations)

        return observations

    # -----------------------------------------------------

    def print_summary(self, observations):

        print("=" * 70)
        print("BLACK BOX OBSERVATION SUMMARY")
        print("=" * 70)

        for i, obs in enumerate(observations, start=1):

            print(f"\nExample {i}")

            for key, value in obs.items():
                print(f"{key:25} : {value}")

        print("=" * 70)