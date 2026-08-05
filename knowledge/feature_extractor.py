"""
============================================================
Universal Feature Extractor (Version 2)
============================================================

Extracts high-level semantic features from ANY dataset.

This module NEVER assumes an algorithm.

It only describes observable characteristics.

Supports

✓ Numbers
✓ Strings
✓ Lists
✓ Tuples
✓ Sets
✓ Dictionaries
✓ Matrices
✓ Graphs
✓ Trees
✓ Optimization
✓ Search
✓ Nested Structures
✓ Context-aware features (future extension)

============================================================
"""

from collections import Counter
from copy import deepcopy


class FeatureExtractor:

    def __init__(self):
        pass

    # =====================================================

    def extract(self, example):

        inp = deepcopy(example.input_data)
        out = deepcopy(example.output_data)

        features = {}

        # --------------------------------------------------
        # Basic Information
        # --------------------------------------------------

        features["input_type"] = type(inp).__name__

        features["output_type"] = type(out).__name__

        features["same_type"] = (

            type(inp) == type(out)

        )

        features["input_size"] = self.safe_length(inp)

        features["output_size"] = self.safe_length(out)

        features["size_preserved"] = (

            self.safe_length(inp)

            ==

            self.safe_length(out)

        )

        # --------------------------------------------------
        # Extract Input Features
        # --------------------------------------------------

        features.update(

            self.extract_features(

                inp,

                "input"

            )

        )

        # --------------------------------------------------
        # Extract Output Features
        # --------------------------------------------------

        features.update(

            self.extract_features(

                out,

                "output"

            )

        )

        # --------------------------------------------------
        # Mapping Features
        # --------------------------------------------------

        features["mapping_type"] = (

            self.detect_mapping(

                inp,

                out

            )

        )

        features["problem_family"] = (

            self.detect_problem_family(

                inp

            )

        )

        features["complexity_hint"] = (

            self.detect_complexity(

                inp

            )

        )

        # --------------------------------------------------
        # Transformation Features
        # --------------------------------------------------

        features.update(

            self.detect_transformations(

                inp,

                out

            )

        )

        return features

    # =====================================================

    def extract_features(

        self,

        obj,

        prefix

    ):

        f = {}

        # --------------------------------------------------
        # Numeric
        # --------------------------------------------------

        if isinstance(obj, (int, float)):

            f[f"{prefix}_numeric"] = True

            f[f"{prefix}_value"] = obj

            f[f"{prefix}_positive"] = obj >= 0

            if isinstance(obj, int):

                f[f"{prefix}_even"] = obj % 2 == 0

                f[f"{prefix}_odd"] = obj % 2 == 1

            return f

        # --------------------------------------------------
        # String
        # --------------------------------------------------

        if isinstance(obj, str):

            f[f"{prefix}_string"] = True

            f[f"{prefix}_length"] = len(obj)

            f[f"{prefix}_empty"] = len(obj) == 0

            f[f"{prefix}_alphabetic"] = obj.isalpha()

            f[f"{prefix}_numeric_string"] = obj.isdigit()

            f[f"{prefix}_uppercase"] = obj.isupper()

            f[f"{prefix}_lowercase"] = obj.islower()

            return f

                # --------------------------------------------------
        # Sequence
        # --------------------------------------------------

        if isinstance(obj, (list, tuple)):

            seq = list(obj)

            f[f"{prefix}_sequence"] = True

            f[f"{prefix}_length"] = len(seq)

            f[f"{prefix}_empty"] = len(seq) == 0

            f[f"{prefix}_duplicates"] = (

                len(seq) != len(set(seq))

            )

            f[f"{prefix}_unique"] = (

                len(seq) == len(set(seq))

            )

            numeric = all(

                isinstance(x, (int, float))

                for x in seq

            )

            f[f"{prefix}_numeric"] = numeric

            if numeric and seq:

                f[f"{prefix}_minimum"] = min(seq)

                f[f"{prefix}_maximum"] = max(seq)

                f[f"{prefix}_sum"] = sum(seq)

                f[f"{prefix}_average"] = (

                    sum(seq) / len(seq)

                )

                f[f"{prefix}_sorted"] = (

                    seq == sorted(seq)

                )

                f[f"{prefix}_reverse_sorted"] = (

                    seq == sorted(seq, reverse=True)

                )

                f[f"{prefix}_even_count"] = sum(

                    1 for x in seq

                    if x % 2 == 0

                )

                f[f"{prefix}_odd_count"] = sum(

                    1 for x in seq

                    if x % 2 == 1

                )

                f[f"{prefix}_all_even"] = all(

                    x % 2 == 0

                    for x in seq

                )

                f[f"{prefix}_all_odd"] = all(

                    x % 2 == 1

                    for x in seq

                )

                f[f"{prefix}_ascending"] = (

                    seq == sorted(seq)

                )

                f[f"{prefix}_descending"] = (

                    seq == sorted(seq, reverse=True)

                )

                f[f"{prefix}_contains_negative"] = any(

                    x < 0

                    for x in seq

                )

                f[f"{prefix}_contains_zero"] = any(

                    x == 0

                    for x in seq

                )

                f[f"{prefix}_range"] = (

                    max(seq) - min(seq)

                )

            # ----------------------------------------------
            # Structural Features
            # ----------------------------------------------

            f[f"{prefix}_nested"] = any(

                isinstance(

                    x,

                    (list, tuple, dict)

                )

                for x in seq

            )

            f[f"{prefix}_matrix"] = (

                all(

                    isinstance(x, list)

                    for x in seq

                )

                if seq

                else False

            )

            return f

                # --------------------------------------------------
        # Dictionary
        # --------------------------------------------------

        if isinstance(obj, dict):

            f[f"{prefix}_dictionary"] = True

            f[f"{prefix}_field_count"] = len(obj)

            f[f"{prefix}_keys"] = sorted(list(obj.keys()))

            f[f"{prefix}_values"] = list(obj.values())

            f[f"{prefix}_empty"] = len(obj) == 0

            f[f"{prefix}_nested_dictionary"] = any(

                isinstance(v, dict)

                for v in obj.values()

            )

            f[f"{prefix}_contains_list"] = any(

                isinstance(v, list)

                for v in obj.values()

            )

            f[f"{prefix}_contains_tuple"] = any(

                isinstance(v, tuple)

                for v in obj.values()

            )

            f[f"{prefix}_contains_set"] = any(

                isinstance(v, set)

                for v in obj.values()

            )

            f[f"{prefix}_contains_numeric"] = any(

                isinstance(v, (int, float))

                for v in obj.values()

            )

            f[f"{prefix}_contains_string"] = any(

                isinstance(v, str)

                for v in obj.values()

            )

            return f

        # --------------------------------------------------
        # Set
        # --------------------------------------------------

        if isinstance(obj, set):

            f[f"{prefix}_set"] = True

            f[f"{prefix}_members"] = len(obj)

            f[f"{prefix}_empty"] = len(obj) == 0

            numeric = all(

                isinstance(x, (int, float))

                for x in obj

            )

            f[f"{prefix}_numeric"] = numeric

            if numeric and obj:

                f[f"{prefix}_minimum"] = min(obj)

                f[f"{prefix}_maximum"] = max(obj)

                f[f"{prefix}_sum"] = sum(obj)

            return f

        # --------------------------------------------------
        # Nested List / Matrix
        # --------------------------------------------------

        if isinstance(obj, list):

            if obj and all(

                isinstance(row, list)

                for row in obj

            ):

                f[f"{prefix}_matrix"] = True

                f[f"{prefix}_rows"] = len(obj)

                f[f"{prefix}_columns"] = (

                    len(obj[0])

                    if obj[0]

                    else 0

                )

                rectangular = all(

                    len(row) == len(obj[0])

                    for row in obj

                )

                f[f"{prefix}_rectangular"] = rectangular

                return f

        # --------------------------------------------------
        # Generic Object
        # --------------------------------------------------

        f[f"{prefix}_object"] = True

        f[f"{prefix}_representation"] = str(type(obj).__name__)

        return f

        # =====================================================
    # Detect Transformations
    # =====================================================

    def detect_transformations(self, inp, out):

        features = {}

        if type(inp) != type(out):

            features["datatype_changed"] = True

            return features

        # --------------------------------------------------
        # Sequence Transformations
        # --------------------------------------------------

        if isinstance(inp, (list, tuple)) and isinstance(out, (list, tuple)):

            inp = list(inp)
            out = list(out)

            features["identity"] = (inp == out)

            features["reverse"] = self.is_reverse(inp, out)

            rotation, amount = self.is_rotation(inp, out)

            features["rotation"] = rotation

            features["rotation_amount"] = amount

            features["stable_partition"] = self.is_stable_partition(inp, out)

            features["even_before_odd"] = self.evens_before_odds(out)

            features["odd_before_even"] = self.odds_before_evens(out)

            features["elements_preserved"] = (

                Counter(inp) == Counter(out)

            )

            features["length_preserved"] = (

                len(inp) == len(out)

            )

            features["sorted_output"] = (

                out == sorted(out)

            )

            features["reverse_sorted_output"] = (

                out == sorted(out, reverse=True)

            )

            features["duplicates_removed"] = (

                len(set(inp)) == len(out)

                and

                Counter(out) == Counter(set(inp))

            )

            features["prefix_preserved"] = self.common_prefix(inp, out)

            features["suffix_preserved"] = self.common_suffix(inp, out)

        return features

        # =====================================================
    # Reverse Detection
    # =====================================================

    def is_reverse(self, inp, out):

        return inp[::-1] == out

    # =====================================================
    # Rotation Detection
    # =====================================================

    def is_rotation(self, inp, out):

        if len(inp) != len(out):

            return False, -1

        n = len(inp)

        for i in range(n):

            if inp[i:] + inp[:i] == out:

                return True, i

        return False, -1

    # =====================================================
    # Stable Partition Detection
    # =====================================================

    def is_stable_partition(self, inp, out):

        if not inp:

            return False

        if not all(isinstance(x, int) for x in inp):

            return False

        even = [x for x in inp if x % 2 == 0]

        odd = [x for x in inp if x % 2 == 1]

        return even + odd == out

    # =====================================================
    # Common Prefix
    # =====================================================

    def common_prefix(self, inp, out):

        count = 0

        for a, b in zip(inp, out):

            if a == b:

                count += 1

            else:

                break

        return count

    # =====================================================
    # Common Suffix
    # =====================================================

    def common_suffix(self, inp, out):

        count = 0

        for a, b in zip(reversed(inp), reversed(out)):

            if a == b:

                count += 1

            else:

                break

        return count

        # =====================================================
    # Even Before Odd
    # =====================================================

    def evens_before_odds(self, seq):

        if not seq:
            return False

        if not all(isinstance(x, int) for x in seq):
            return False

        found_odd = False

        for value in seq:

            if value % 2 == 1:
                found_odd = True

            elif found_odd:
                return False

        return True

    # =====================================================
    # Odd Before Even
    # =====================================================

    def odds_before_evens(self, seq):

        if not seq:
            return False

        if not all(isinstance(x, int) for x in seq):
            return False

        found_even = False

        for value in seq:

            if value % 2 == 0:
                found_even = True

            elif found_even:
                return False

        return True

    # =====================================================
    # Detect Mapping
    # =====================================================

    def detect_mapping(self, inp, out):

        if type(inp) != type(out):
            return "datatype_transformation"

        if isinstance(inp, (list, tuple)):

            inp = list(inp)
            out = list(out)

            if inp == out:
                return "identity"

            if inp[::-1] == out:
                return "reverse"

            rotation, _ = self.is_rotation(inp, out)

            if rotation:
                return "rotation"

            if self.is_stable_partition(inp, out):
                return "stable_partition"

            if Counter(inp) == Counter(out):
                return "reordering"

            return "sequence_transformation"

        if isinstance(inp, dict):
            return "dictionary_mapping"

        if isinstance(inp, str):

            if inp == out:
                return "identity"

            if inp[::-1] == out:
                return "reverse_string"

            return "string_transformation"

        if isinstance(inp, (int, float)):
            return "numeric_transformation"

        return "generic"

        # =====================================================
    # Detect Problem Family
    # =====================================================

    def detect_problem_family(self, inp):

        if isinstance(inp, dict):

            keys = set(inp.keys())

            if {"weights", "values", "capacity"} <= keys:
                return "optimization"

            if {"graph", "edges"} & keys:
                return "graph"

            if {"tree", "root"} & keys:
                return "tree"

            if {"matrix"} <= keys:
                return "matrix"

            if {"array", "target"} <= keys:
                return "search"

            if {"text", "pattern"} <= keys:
                return "pattern_matching"

            if {"points"} <= keys:
                return "geometry"

            return "structured_data"

        if isinstance(inp, (list, tuple)):

            if all(isinstance(x, (int, float)) for x in inp):
                return "numeric_sequence"

            return "sequence"

        if isinstance(inp, str):
            return "string"

        if isinstance(inp, (int, float)):
            return "numeric"

        return "generic"

    # =====================================================
    # Detect Complexity
    # =====================================================

    def detect_complexity(self, inp):

        if isinstance(inp, dict):

            complexity = len(inp)

            for value in inp.values():

                complexity += self.safe_length(value)

            return complexity

        if isinstance(inp, (list, tuple, set)):
            return len(inp)

        if isinstance(inp, str):
            return len(inp)

        return 1

    # =====================================================
    # Safe Length
    # =====================================================

    def safe_length(self, obj):

        try:
            return len(obj)

        except Exception:
            return 1