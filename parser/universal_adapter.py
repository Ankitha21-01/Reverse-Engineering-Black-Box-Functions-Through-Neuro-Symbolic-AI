"""
=========================================================
Universal Adapter
=========================================================

Converts every datatype into one unified representation
without changing semantic meaning.

=========================================================
"""


class UniversalAdapter:

    def adapt(self, obj):

        if obj is None:
            return None

        if isinstance(obj, (int, float, bool, str)):
            return obj

        if isinstance(obj, tuple):
            return [self.adapt(x) for x in obj]

        if isinstance(obj, set):
            return [self.adapt(x) for x in sorted(obj)]

        if isinstance(obj, list):
            return [self.adapt(x) for x in obj]

        if isinstance(obj, dict):

            result = {}

            for k, v in obj.items():

                result[str(k)] = self.adapt(v)

            return result

        return str(obj)