"""
============================================================
Universal Fact Generator
============================================================

Generates symbolic facts from ANY datatype.

Supports

✓ Numbers
✓ Strings
✓ Lists
✓ Tuples
✓ Dictionaries
✓ Sets
✓ Matrices
✓ Graphs
✓ Trees
✓ Nested Structures
✓ Unknown Structures

This module NEVER assumes any algorithm.

============================================================
"""


class FactGenerator:

    def generate(self, example):

        facts = []

        self._generate(
            example.input_data,
            "input",
            facts
        )

        self._generate(
            example.output_data,
            "output",
            facts
        )

        return facts

    # =====================================================

    def _generate(self, obj, prefix, facts):

        # -------------------------------------------------
        # None
        # -------------------------------------------------

        if obj is None:

            facts.append(f"{prefix}_null")

            return

        # -------------------------------------------------
        # Boolean
        # -------------------------------------------------

        if isinstance(obj, bool):

            facts.append(f"{prefix}_boolean({str(obj).lower()})")

            return

        # -------------------------------------------------
        # Number
        # -------------------------------------------------

        if isinstance(obj, (int, float)):

            facts.append(f"{prefix}_number({repr(obj)})")

            return

        # -------------------------------------------------
        # String
        # -------------------------------------------------

        if isinstance(obj, str):

            facts.append(
                f'{prefix}_string("{obj}")'
            )

            facts.append(
                f"{prefix}_length({len(obj)})"
            )

            return

        # -------------------------------------------------
        # List / Tuple
        # -------------------------------------------------

        if isinstance(obj, (list, tuple)):

            facts.append(
                f"{prefix}_sequence({len(obj)})"
            )

            for i, value in enumerate(obj):

                facts.append(
                    f"{prefix}_index({i})"
                )

                self._generate(
                    value,
                    f"{prefix}_{i}",
                    facts
                )

            return

        # -------------------------------------------------
        # Dictionary
        # -------------------------------------------------

        if isinstance(obj, dict):

            facts.append(
                f"{prefix}_dictionary({len(obj)})"
            )

            for key, value in obj.items():

                facts.append(
                    f'{prefix}_key("{key}")'
                )

                self._generate(
                    value,
                    f"{prefix}_{key}",
                    facts
                )

            return

        # -------------------------------------------------
        # Set
        # -------------------------------------------------

        if isinstance(obj, set):

            facts.append(
                f"{prefix}_set({len(obj)})"
            )

            for value in sorted(obj):

                self._generate(
                    value,
                    prefix,
                    facts
                )

            return

        # -------------------------------------------------
        # Generic Object
        # -------------------------------------------------

        facts.append(

            f"{prefix}_object('{repr(obj)}')"

        )