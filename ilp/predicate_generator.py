"""
=========================================================
Universal Predicate Generator
=========================================================

Generates symbolic predicates from discovered knowledge.

Supports KnowledgeObject or dictionary-based knowledge.

No algorithm-specific assumptions.

=========================================================
"""


class PredicateGenerator:

    def __init__(self):
        pass

    # =====================================================

    def generate(self, knowledge):

        predicates = []

        # -----------------------------------------
        # Support both KnowledgeObject and dict
        # -----------------------------------------

        if hasattr(knowledge, "properties"):

            properties = knowledge.properties
            relations = knowledge.relations
            facts = knowledge.facts

        else:

            properties = knowledge.get("properties", {})
            relations = knowledge.get("relations", [])
            facts = knowledge.get("facts", [])

        # -----------------------------------------
        # Properties
        # -----------------------------------------

        for key, value in properties.items():

            key = str(key).strip()

            if not key:
                continue

            if isinstance(value, bool):

                if value:
                    predicates.append(key)

            elif isinstance(value, (list, tuple, set)):

                for item in value:

                    if item is None:
                        continue

                    predicates.append(

                        f"{key}({repr(item)})"

                    )

            elif value is not None:

                predicates.append(

                    f"{key}({repr(value)})"

                )

        # -----------------------------------------
        # Relations
        # -----------------------------------------

        for relation in relations:

            if isinstance(relation, dict):

                relation_name = str(

                    relation.get(

                        "relation",

                        "relation"

                    )

                ).strip()

                arguments = []

                for k, v in relation.items():

                    if k == "relation":
                        continue

                    if v is None:
                        continue

                    arguments.append(

                        repr(v)

                    )

                if arguments:

                    predicates.append(

                        f"{relation_name}({','.join(arguments)})"

                    )

                else:

                    predicates.append(

                        relation_name

                    )

            elif relation:

                predicates.append(

                    str(relation)

                )

        # -----------------------------------------
        # Facts
        # -----------------------------------------

        for fact in facts:

            if fact:

                predicates.append(

                    str(fact)

                )

        # -----------------------------------------
        # Remove duplicates
        # -----------------------------------------

        predicates = sorted(

            set(predicates)

        )

        return predicates