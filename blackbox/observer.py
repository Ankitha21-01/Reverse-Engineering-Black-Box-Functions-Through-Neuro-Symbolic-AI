"""
============================================================
Universal BlackBox Observer
============================================================

Observes only input-output behaviour.

No algorithm assumptions.

============================================================
"""

from collections import Counter


class BlackBoxObserver:

    def observe(self, input_data, output_data):

        observation = {}

        observation["input_type"] = type(input_data).__name__
        observation["output_type"] = type(output_data).__name__

        observation["same_type"] = (
            type(input_data) == type(output_data)
        )

        observation["input_size"] = self.size(input_data)
        observation["output_size"] = self.size(output_data)

        observation["size_preserved"] = (
            observation["input_size"] ==
            observation["output_size"]
        )

        observation["value_preserved"] = self.values_preserved(
            input_data,
            output_data
        )

        observation["structure_changed"] = (
            str(type(input_data)) != str(type(output_data))
        )

        observation["detected_domain"] = self.detect_domain(input_data)

        return observation

    # -----------------------------------------------------

    def size(self, obj):

        try:
            return len(obj)
        except Exception:
            return 1

    # -----------------------------------------------------

    def values_preserved(self, inp, out):

        if isinstance(inp, (list, tuple)) and isinstance(out, (list, tuple)):
            return Counter(inp) == Counter(out)

        return False

    # -----------------------------------------------------

    def detect_domain(self, obj):

        if isinstance(obj, dict):

            keys = set(obj.keys())

            if {"weights", "values", "capacity"} <= keys:
                return "optimization"

            if {"edges", "vertices"} <= keys:
                return "graph"

            if {"matrix"} <= keys:
                return "matrix"

            if {"array", "target"} <= keys:
                return "search"

            return "structured"

        if isinstance(obj, list):

            if all(isinstance(i, list) for i in obj):
                return "matrix"

            return "sequence"

        if isinstance(obj, str):
            return "string"

        if isinstance(obj, (int, float)):
            return "numeric"

        return "generic"