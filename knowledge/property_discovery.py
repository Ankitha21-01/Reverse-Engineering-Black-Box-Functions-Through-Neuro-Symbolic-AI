"""
=========================================================
Universal Property Discovery (Version 2)
=========================================================

Automatically discovers observable symbolic properties
from input-output examples.

Goals

✓ Domain independent
✓ Algorithm independent
✓ Rich symbolic properties
✓ Structural comparison
✓ Supports future Context Engine

=========================================================
"""

from collections import Counter
from copy import deepcopy


class PropertyDiscovery:

    def __init__(self):
        pass

    # =====================================================

    def discover(self, example):

        properties = {}

        inp = deepcopy(example.input_data)
        out = deepcopy(example.output_data)

        # -------------------------------------------------
        # Basic datatype information
        # -------------------------------------------------

        properties["input_type"] = type(inp).__name__
        properties["output_type"] = type(out).__name__

        properties["same_type"] = (
            type(inp) == type(out)
        )

        properties["input_is_number"] = isinstance(
            inp,
            (int, float)
        )

        properties["output_is_number"] = isinstance(
            out,
            (int, float)
        )

        properties["input_is_string"] = isinstance(
            inp,
            str
        )

        properties["output_is_string"] = isinstance(
            out,
            str
        )

        properties["input_is_sequence"] = isinstance(
            inp,
            (list, tuple, set)
        )

        properties["output_is_sequence"] = isinstance(
            out,
            (list, tuple, set)
        )

        properties["input_is_dictionary"] = isinstance(
            inp,
            dict
        )

        properties["output_is_dictionary"] = isinstance(
            out,
            dict
        )

        # -------------------------------------------------
        # Length
        # -------------------------------------------------

        properties["input_length"] = self.safe_length(inp)

        properties["output_length"] = self.safe_length(out)

        properties["length_preserved"] = (

            properties["input_length"]

            ==

            properties["output_length"]

        )

        properties["size_difference"] = (

            properties["output_length"]

            -

            properties["input_length"]

        )

        # -------------------------------------------------
        # Empty structures
        # -------------------------------------------------

        properties["input_empty"] = (

            properties["input_length"] == 0

        )

        properties["output_empty"] = (

            properties["output_length"] == 0

        )

        # -------------------------------------------------
        # Numeric values
        # -------------------------------------------------

        if isinstance(inp, (int, float)):

            properties["input_positive"] = inp >= 0

            properties["input_negative"] = inp < 0

            properties["input_zero"] = inp == 0

            if isinstance(inp, int):

                properties["input_even"] = (

                    inp % 2 == 0

                )

                properties["input_odd"] = (

                    inp % 2 == 1

                )

        if isinstance(out, (int, float)):

            properties["output_positive"] = out >= 0

            properties["output_negative"] = out < 0

            properties["output_zero"] = out == 0

            if isinstance(out, int):

                properties["output_even"] = (

                    out % 2 == 0

                )

                properties["output_odd"] = (

                    out % 2 == 1

                )

        # -------------------------------------------------
        # Sequence properties
        # -------------------------------------------------

        if isinstance(inp, (list, tuple, set)):

            properties.update(

                self.sequence_properties(

                    list(inp),

                    "input"

                )

            )

        if isinstance(out, (list, tuple, set)):

            properties.update(

                self.sequence_properties(

                    list(out),

                    "output"

                )

            )

        # -------------------------------------------------
        # Generic sequence comparison
        # -------------------------------------------------

        if isinstance(inp, (list, tuple, set)) and isinstance(
            out,
            (list, tuple, set)
        ):

            in_list = list(inp)
            out_list = list(out)

            properties.update(

                self.compare_sequences(

                    in_list,

                    out_list

                )

            )

        # -------------------------------------------------
        # Dictionary structure
        # -------------------------------------------------

        if isinstance(inp, dict):

            properties.update(

                self.dictionary_properties(

                    inp,

                    "input"

                )

            )

        if isinstance(out, dict):

            properties.update(

                self.dictionary_properties(

                    out,

                    "output"

                )

            )

        # -------------------------------------------------
        # Matrix structure
        # -------------------------------------------------

        properties["input_is_matrix"] = self.is_matrix(inp)

        properties["output_is_matrix"] = self.is_matrix(out)

        if properties["input_is_matrix"]:

            properties["input_rows"] = len(inp)

            properties["input_columns"] = len(inp[0])

        if properties["output_is_matrix"]:

            properties["output_rows"] = len(out)

            properties["output_columns"] = len(out[0])

        # -------------------------------------------------
        # Generic structural properties
        # -------------------------------------------------

        properties["input_hashable"] = self.is_hashable(inp)

        properties["output_hashable"] = self.is_hashable(out)

        properties["input_repr"] = type(inp).__name__

        properties["output_repr"] = type(out).__name__

        properties["nested_input"] = self.has_nested_structure(inp)

        properties["nested_output"] = self.has_nested_structure(out)

        properties["contains_dictionary"] = self.contains_dictionary(inp)

        properties["contains_sequence"] = self.contains_sequence(inp)

        properties["contains_numbers"] = self.contains_numbers(inp)

        properties["contains_strings"] = self.contains_strings(inp)

        return properties

            # =====================================================
    # Compare Input and Output Sequences
    # =====================================================

    def compare_sequences(self, inp, out):

        p = {}

        p["values_preserved"] = (
            Counter(inp) == Counter(out)
        )

        p["same_multiset"] = p["values_preserved"]

        p["order_preserved"] = (
            inp == out
        )

        p["order_changed"] = (
            inp != out
        )

        p["same_length"] = (
            len(inp) == len(out)
        )

        p["unique_count_preserved"] = (
            len(set(inp)) == len(set(out))
        )

        p["duplicate_count_preserved"] = (
            len(inp) - len(set(inp))
            ==
            len(out) - len(set(out))
        )

        if inp:

            p["first_element_preserved"] = (
                inp[0] == out[0]
            )

            p["last_element_preserved"] = (
                inp[-1] == out[-1]
            )

        else:

            p["first_element_preserved"] = False
            p["last_element_preserved"] = False

        p["is_reverse"] = (
            out == list(reversed(inp))
        )

        p["rotation_detected"] = self.is_rotation(
            inp,
            out
        )

        p["prefix_preserved"] = self.prefix_preserved(
            inp,
            out
        )

        p["suffix_preserved"] = self.suffix_preserved(
            inp,
            out
        )

        p["common_elements"] = len(
            set(inp).intersection(set(out))
        )

        p["new_elements"] = len(
            set(out) - set(inp)
        )

        p["removed_elements"] = len(
            set(inp) - set(out)
        )

        # ------------------------------------------
        # Numeric symbolic properties
        # ------------------------------------------

        numeric = all(
            isinstance(x, (int, float))
            for x in inp + out
        )

        p["numeric_sequence"] = numeric

        if numeric:

            p["input_even_count"] = sum(
                1 for x in inp
                if isinstance(x, int) and x % 2 == 0
            )

            p["input_odd_count"] = sum(
                1 for x in inp
                if isinstance(x, int) and x % 2 == 1
            )

            p["output_even_count"] = sum(
                1 for x in out
                if isinstance(x, int) and x % 2 == 0
            )

            p["output_odd_count"] = sum(
                1 for x in out
                if isinstance(x, int) and x % 2 == 1
            )

            p["sum_preserved"] = (
                sum(inp) == sum(out)
            )

            p["minimum_preserved"] = (
                min(inp) == min(out)
            )

            p["maximum_preserved"] = (
                max(inp) == max(out)
            )

            p["mean_preserved"] = (
                sum(inp) / len(inp)
                ==
                sum(out) / len(out)
            )

            p["sorted_input"] = (
                inp == sorted(inp)
            )

            p["sorted_output"] = (
                out == sorted(out)
            )

            p["output_even_prefix"] = self.even_prefix(out)

            p["output_odd_suffix"] = self.odd_suffix(out)

        return p

    # =====================================================
    # Dictionary Properties
    # =====================================================

    def dictionary_properties(self, d, prefix):

        p = {}

        p[f"{prefix}_keys"] = sorted(
            d.keys()
        )

        p[f"{prefix}_key_count"] = len(d)

        p[f"{prefix}_contains_nested"] = any(
            isinstance(v, (dict, list, tuple))
            for v in d.values()
        )

        for key, value in d.items():

            p[f"{prefix}_{key}_type"] = (
                type(value).__name__
            )

            p[f"{prefix}_{key}_length"] = (
                self.safe_length(value)
            )

        return p

    # =====================================================
    # Rotation Detection
    # =====================================================

    def is_rotation(self, a, b):

        if len(a) != len(b):
            return False

        if not a:
            return True

        doubled = a + a

        n = len(a)

        for i in range(n):

            if doubled[i:i+n] == b:
                return True

        return False

    # =====================================================
    # Prefix Preservation
    # =====================================================

    def prefix_preserved(self, a, b):

        if not a or not b:
            return False

        limit = min(len(a), len(b))

        for i in range(limit):

            if a[i] != b[i]:
                return i > 0

        return True

    # =====================================================
    # Suffix Preservation
    # =====================================================

    def suffix_preserved(self, a, b):

        if not a or not b:
            return False

        i = 1

        preserved = False

        while i <= min(len(a), len(b)):

            if a[-i] != b[-i]:
                break

            preserved = True

            i += 1

        return preserved
        # =====================================================
    # Even Prefix Detection
    # =====================================================

    def even_prefix(self, seq):

        if not seq:
            return False

        encountered_odd = False

        for value in seq:

            if not isinstance(value, int):
                return False

            if value % 2 == 0:

                if encountered_odd:
                    return False

            else:

                encountered_odd = True

        return True

    # =====================================================
    # Odd Suffix Detection
    # =====================================================

    def odd_suffix(self, seq):

        if not seq:
            return False

        encountered_odd = False

        for value in reversed(seq):

            if not isinstance(value, int):
                return False

            if value % 2 == 1:

                encountered_odd = True

            else:

                if encountered_odd:
                    return False

        return True

    # =====================================================
    # Improved Sequence Properties
    # =====================================================

    def sequence_properties(self, seq, prefix):

        p = {}

        p[f"{prefix}_duplicates"] = (
            len(seq) != len(set(seq))
        )

        p[f"{prefix}_unique"] = (
            len(seq) == len(set(seq))
        )

        p[f"{prefix}_empty"] = (
            len(seq) == 0
        )

        p[f"{prefix}_length"] = len(seq)

        p[f"{prefix}_nested"] = any(
            isinstance(x, (list, tuple, dict))
            for x in seq
        )

        numeric = all(
            isinstance(x, (int, float))
            for x in seq
        )

        p[f"{prefix}_numeric"] = numeric

        if numeric and seq:

            p[f"{prefix}_minimum"] = min(seq)

            p[f"{prefix}_maximum"] = max(seq)

            p[f"{prefix}_sum"] = sum(seq)

            p[f"{prefix}_average"] = (
                sum(seq) / len(seq)
            )

            p[f"{prefix}_sorted"] = (
                seq == sorted(seq)
            )

            p[f"{prefix}_strictly_increasing"] = all(
                seq[i] < seq[i + 1]
                for i in range(len(seq) - 1)
            )

            p[f"{prefix}_strictly_decreasing"] = all(
                seq[i] > seq[i + 1]
                for i in range(len(seq) - 1)
            )

            p[f"{prefix}_all_even"] = all(
                isinstance(x, int) and x % 2 == 0
                for x in seq
            )

            p[f"{prefix}_all_odd"] = all(
                isinstance(x, int) and x % 2 == 1
                for x in seq
            )

        return p

    # =====================================================
    # Safe Length
    # =====================================================

    def safe_length(self, obj):

        try:
            return len(obj)
        except Exception:
            return 1

    # =====================================================
    # Hashable Check
    # =====================================================

    def is_hashable(self, obj):

        try:
            hash(obj)
            return True
        except Exception:
            return False

    # =====================================================
    # Matrix Detection
    # =====================================================

    def is_matrix(self, obj):

        if not isinstance(obj, list):
            return False

        if not obj:
            return False

        return all(
            isinstance(row, list)
            for row in obj
        )

    # =====================================================
    # Nested Structure
    # =====================================================

    def has_nested_structure(self, obj):

        if isinstance(obj, dict):
            return True

        if isinstance(obj, (list, tuple)):

            return any(
                isinstance(
                    x,
                    (list, tuple, dict)
                )
                for x in obj
            )

        return False

    # =====================================================
    # Contains Dictionary
    # =====================================================

    def contains_dictionary(self, obj):

        if isinstance(obj, dict):
            return True

        if isinstance(obj, (list, tuple)):

            return any(
                isinstance(x, dict)
                for x in obj
            )

        return False

    # =====================================================
    # Contains Sequence
    # =====================================================

    def contains_sequence(self, obj):

        if isinstance(obj, (list, tuple)):
            return True

        if isinstance(obj, dict):

            return any(
                isinstance(v, (list, tuple))
                for v in obj.values()
            )

        return False

    # =====================================================
    # Contains Numbers
    # =====================================================

    def contains_numbers(self, obj):

        if isinstance(obj, (int, float)):
            return True

        if isinstance(obj, (list, tuple)):

            return any(
                isinstance(x, (int, float))
                for x in obj
            )

        if isinstance(obj, dict):

            return any(
                isinstance(v, (int, float))
                for v in obj.values()
            )

        return False

    # =====================================================
    # Contains Strings
    # =====================================================

    def contains_strings(self, obj):

        if isinstance(obj, str):
            return True

        if isinstance(obj, (list, tuple)):

            return any(
                isinstance(x, str)
                for x in obj
            )

        if isinstance(obj, dict):

            return any(
                isinstance(v, str)
                for v in obj.values()
            )

        return False