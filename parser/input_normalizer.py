"""
=========================================================
Universal Input Normalizer
=========================================================

Converts CSV values into native Python objects.

Supports

✓ Integer
✓ Float
✓ Boolean
✓ None
✓ String
✓ List
✓ Tuple
✓ Set
✓ Dictionary
✓ Nested Objects
✓ Matrix
✓ Graph
✓ Generic Structures

=========================================================
"""

import ast


class InputNormalizer:

    def normalize(self, value):

        if isinstance(value, dict):

            normalized = {}

            for k, v in value.items():
                normalized[str(k)] = self.normalize(v)

            return normalized

        if isinstance(value, list):

            return [
                self.normalize(v)
                for v in value
            ]

        if isinstance(value, tuple):

            return [
                self.normalize(v)
                for v in value
            ]

        if isinstance(value, set):

            return sorted([
                self.normalize(v)
                for v in value
            ])

        if value is None:
            return None

        if isinstance(value, (int, float, bool)):
            return value

        text = str(value).strip()

        if text == "":
            return ""

        lower = text.lower()

        if lower == "true":
            return True

        if lower == "false":
            return False

        if lower in ("none", "null", "nan"):
            return None

        try:
            return int(text)
        except:
            pass

        try:
            return float(text)
        except:
            pass

        try:
            parsed = ast.literal_eval(text)
            return self.normalize(parsed)
        except:
            pass

        return text