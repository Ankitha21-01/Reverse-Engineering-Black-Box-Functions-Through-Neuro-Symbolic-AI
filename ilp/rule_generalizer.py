"""
=========================================================
Universal Rule Generalizer
=========================================================

Generalizes learned symbolic rules.

Performs

✓ Duplicate removal
✓ Predicate normalization
✓ Rule normalization
✓ Rule simplification
✓ Rule signature generation

No algorithm-specific assumptions.

=========================================================
"""


class RuleGeneralizer:

    def __init__(self):
        pass

    # =====================================================

    def generalize(self, hypotheses):

        generalized = []

        signatures = set()

        for hypothesis in hypotheses:

            # ---------------------------------------------
            # Normalize predicates
            # ---------------------------------------------

            predicates = []

            seen_predicates = set()

            for predicate in hypothesis.get("predicates", []):

                predicate = str(predicate).strip()

                if not predicate:
                    continue

                if predicate in seen_predicates:
                    continue

                seen_predicates.add(predicate)
                predicates.append(predicate)

            predicates.sort()

            # ---------------------------------------------
            # Normalize rules
            # ---------------------------------------------

            rules = []

            seen_rules = set()

            for rule in hypothesis.get("rules", []):

                rule = str(rule).strip()

                if not rule:
                    continue

                if not rule.endswith("."):
                    rule += "."

                if rule in seen_rules:
                    continue

                seen_rules.add(rule)
                rules.append(rule)

            # Preserve original rule order.
            # Only remove duplicates.

            # ---------------------------------------------
            # Generalization signature
            # ---------------------------------------------

            signature = (

                tuple(predicates),

                tuple(rules)

            )

            if signature in signatures:
                continue

            signatures.add(signature)

            # ---------------------------------------------
            # Build generalized hypothesis
            # ---------------------------------------------

            new_hypothesis = dict(hypothesis)

            new_hypothesis["predicates"] = predicates
            new_hypothesis["rules"] = rules

            new_hypothesis["predicate_count"] = len(predicates)
            new_hypothesis["rule_count"] = len(rules)

            new_hypothesis["generalized"] = True

            generalized.append(new_hypothesis)

        return generalized