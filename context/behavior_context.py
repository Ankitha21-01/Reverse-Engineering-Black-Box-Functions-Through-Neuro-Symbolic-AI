"""
============================================================
Universal Behaviour Context
============================================================
"""


class BehaviorContext:

    def extract(self, knowledge):

        behaviours = set()

        for item in knowledge:

            for relation in item.relations:

                if isinstance(relation, dict):

                    behaviours.add(
                        relation.get(
                            "relation",
                            "unknown"
                        )
                    )

                else:

                    behaviours.add(str(relation))

        return sorted(behaviours)