"""
=========================================================
Universal Predicate Refiner
=========================================================

Refines learned predicates by

✓ Removing duplicates
✓ Removing empty predicates
✓ Removing malformed predicates
✓ Removing contradictory boolean predicates
✓ Sorting predicates for deterministic learning

No algorithm-specific assumptions.

=========================================================
"""


class PredicateRefiner:

    def __init__(self):
        pass

    # =====================================================

    def refine(self, hypotheses):

        refined = []

        for hypothesis in hypotheses:

            predicates = hypothesis.get("predicates", [])

            cleaned = []

            seen = set()

            for predicate in predicates:

                predicate = str(predicate).strip()

                if not predicate:
                    continue

                # Skip malformed predicates
                if "None" in predicate:
                    continue

                if predicate in seen:
                    continue

                seen.add(predicate)
                cleaned.append(predicate)

            # ---------------------------------------------
            # Remove contradictory boolean predicates
            # Example:
            # input_numeric
            # not_input_numeric
            # ---------------------------------------------

            final_predicates = []

            predicate_set = set(cleaned)

            for predicate in cleaned:

                if predicate.startswith("not_"):

                    positive = predicate[4:]

                    if positive in predicate_set:
                        continue

                final_predicates.append(predicate)

            final_predicates.sort()

            new_hypothesis = dict(hypothesis)

            new_hypothesis["predicates"] = final_predicates

            new_hypothesis["predicate_count"] = len(final_predicates)

            refined.append(new_hypothesis)

        return refined