"""
============================================================
Universal Pattern Context
============================================================
"""

from collections import Counter


class PatternContext:

    def extract(self, knowledge):

        counter = Counter()

        for item in knowledge:

            for key in item.properties.keys():
                counter[key] += 1

            for relation in item.relations:

                if isinstance(relation, dict):

                    counter[
                        relation.get(
                            "relation",
                            "unknown"
                        )
                    ] += 1

                else:

                    counter[str(relation)] += 1

        patterns = []

        for key, value in counter.items():

            patterns.append(
                f"{key} observed {value} time(s)"
            )

        return patterns