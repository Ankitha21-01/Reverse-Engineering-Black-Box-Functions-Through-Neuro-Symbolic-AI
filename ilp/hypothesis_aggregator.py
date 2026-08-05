"""
=========================================================
Universal Hypothesis Aggregator
=========================================================

Combines similar symbolic hypotheses.

Performs

✓ Duplicate removal
✓ Rule-based similarity checking
✓ Predicate merging
✓ Confidence preservation
✓ Hypothesis consolidation

No algorithm-specific assumptions.

=========================================================
"""


class HypothesisAggregator:

    def __init__(self):
        pass

    # =====================================================

    def aggregate(self, hypotheses):

        aggregated = []

        signatures = {}

        for hypothesis in hypotheses:

            predicates = sorted(
                set(
                    hypothesis.get(
                        "predicates",
                        []
                    )
                )
            )

            rules = sorted(
                set(
                    hypothesis.get(
                        "rules",
                        []
                    )
                )
            )

            signature = (

                tuple(predicates),

                tuple(rules)

            )

            # ---------------------------------------------
            # Merge similar hypotheses
            # ---------------------------------------------

            if signature in signatures:

                existing = signatures[signature]

                existing["confidence"] = max(

                    existing.get(
                        "confidence",
                        0
                    ),

                    hypothesis.get(
                        "confidence",
                        0
                    )

                )

                existing["description"] = (

                    existing.get(
                        "description",
                        ""
                    )

                    +

                    " | "

                    +

                    hypothesis.get(
                        "description",
                        ""
                    )

                )

                continue


            # ---------------------------------------------
            # Create new aggregated hypothesis
            # ---------------------------------------------

            new_hypothesis = dict(hypothesis)

            new_hypothesis["predicates"] = predicates

            new_hypothesis["rules"] = rules

            new_hypothesis["predicate_count"] = len(
                predicates
            )

            new_hypothesis["rule_count"] = len(
                rules
            )

            new_hypothesis["aggregated"] = True


            signatures[signature] = new_hypothesis

            aggregated.append(
                new_hypothesis
            )


        # ---------------------------------------------
        # Highest confidence hypotheses first
        # ---------------------------------------------

        aggregated.sort(

            key=lambda h: h.get(
                "confidence",
                0
            ),

            reverse=True

        )


        return aggregated