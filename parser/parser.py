"""
=========================================================
Dataset Parser
=========================================================

Converts CSV rows into universal TrainingExample objects.

=========================================================
"""

from utils.models import TrainingExample
from parser.input_normalizer import InputNormalizer
from parser.universal_adapter import UniversalAdapter


class DatasetParser:

    def __init__(self):

        self.normalizer = InputNormalizer()
        self.adapter = UniversalAdapter()

    def parse(self, input_df, output_df, context=None):

        dataset = []

        rows = min(len(input_df), len(output_df))

        for index in range(rows):

            raw_input = input_df.iloc[index].to_dict()
            raw_output = output_df.iloc[index].to_dict()

            input_data = self.adapter.adapt(

                self.normalizer.normalize(raw_input)

            )

            output_data = self.adapter.adapt(

                self.normalizer.normalize(raw_output)

            )

            dataset.append(

                TrainingExample(

                    example_id=index + 1,

                    input_data=input_data,

                    output_data=output_data,

                    context=context,

                    metadata={

                        "input_columns": list(input_df.columns),

                        "output_columns": list(output_df.columns)

                    }

                )

            )

        return dataset