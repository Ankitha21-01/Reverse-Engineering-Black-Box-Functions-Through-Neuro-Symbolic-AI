"""
============================================================
Universal Helper Functions
============================================================

Generic utility functions used throughout the framework.

============================================================
"""

import ast
import copy


class Helper:

    # -----------------------------------------------------

    @staticmethod
    def parse_input(text):

        text = str(text).strip()

        try:

            return ast.literal_eval(text)

        except Exception:

            return text

    # -----------------------------------------------------

    @staticmethod
    def deep_copy(obj):

        return copy.deepcopy(obj)

    # -----------------------------------------------------

    @staticmethod
    def safe_length(obj):

        try:

            return len(obj)

        except Exception:

            return 1

    # -----------------------------------------------------

    @staticmethod
    def is_numeric(value):

        return isinstance(value, (int, float))

    # -----------------------------------------------------

    @staticmethod
    def is_sequence(value):

        return isinstance(value, (list, tuple))

    # -----------------------------------------------------

    @staticmethod
    def is_dictionary(value):

        return isinstance(value, dict)

    # -----------------------------------------------------

    @staticmethod
    def flatten(data):

        result = []

        if isinstance(data, list):

            for item in data:

                if isinstance(item, list):

                    result.extend(

                        Helper.flatten(item)

                    )

                else:

                    result.append(item)

        else:

            result.append(data)

        return result

    # -----------------------------------------------------

    @staticmethod
    def unique(sequence):

        result = []

        for item in sequence:

            if item not in result:

                result.append(item)

        return result

    # -----------------------------------------------------

    @staticmethod
    def print_title(title):

        print("\n" + "=" * 70)

        print(title)

        print("=" * 70)

    # -----------------------------------------------------

    @staticmethod
    def print_dictionary(dictionary):

        for key, value in dictionary.items():

            print(f"{key:30}: {value}")

    # -----------------------------------------------------

    @staticmethod
    def normalize_key(key):

        return str(key).strip().lower().replace(" ", "_")