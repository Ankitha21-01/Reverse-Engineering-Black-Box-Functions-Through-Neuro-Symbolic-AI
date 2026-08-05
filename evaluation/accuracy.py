"""
=========================================================
Universal Accuracy Evaluation
=========================================================

Supports

✓ Numbers
✓ Strings
✓ Lists
✓ Tuples
✓ Dictionaries
✓ Sets
✓ Nested Objects

=========================================================
"""

from collections import Counter


class Accuracy:

    def __init__(self):
        pass

    # =====================================================

    def score(

        self,

        expected,

        predicted

    ):

        if type(expected) != type(predicted):

            return 0.0

        # ----------------------------------

        if expected == predicted:

            return 1.0

        # ----------------------------------

        if isinstance(expected, (list, tuple)):

            return self.sequence_accuracy(

                expected,

                predicted

            )

        # ----------------------------------

        if isinstance(expected, dict):

            return self.dictionary_accuracy(

                expected,

                predicted

            )

        # ----------------------------------

        if isinstance(expected, set):

            return self.set_accuracy(

                expected,

                predicted

            )

        return 0.0

    # =====================================================

    def sequence_accuracy(

        self,

        expected,

        predicted

    ):

        if len(expected) == 0:

            return 1.0

        correct = sum(

            1

            for a, b in zip(expected, predicted)

            if a == b

        )

        return round(

            correct / max(len(expected), len(predicted)),

            3

        )

    # =====================================================

    def dictionary_accuracy(

        self,

        expected,

        predicted

    ):

        keys = set(expected.keys()) | set(predicted.keys())

        if not keys:

            return 1.0

        correct = 0

        for key in keys:

            if expected.get(key) == predicted.get(key):

                correct += 1

        return round(correct / len(keys), 3)

    # =====================================================

    def set_accuracy(

        self,

        expected,

        predicted

    ):

        intersection = len(expected & predicted)

        union = len(expected | predicted)

        if union == 0:

            return 1.0

        return round(intersection / union, 3)