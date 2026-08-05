"""
============================================================
Universal Semantic Context
============================================================
"""


class SemanticContext:

    def extract(self, knowledge):

        semantics = set()

        for item in knowledge:

            for key, value in item.properties.items():
                semantics.add(f"{key} : {value}")

            for key, value in item.features.items():
                semantics.add(f"{key} : {value}")

        return sorted(semantics)