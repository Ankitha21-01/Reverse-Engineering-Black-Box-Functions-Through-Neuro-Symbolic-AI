"""
=========================================================
Rule Normalizer
=========================================================

Normalizes Prolog rules.

=========================================================
"""


class RuleNormalizer:

    def normalize(self, hypotheses):

        normalized = []

        for hypothesis in hypotheses:

            rules = []
            seen = set()

            for rule in hypothesis.get("rules", []):

                rule = " ".join(str(rule).split()).strip()

                if not rule:
                    continue

                if not rule.endswith("."):
                    rule += "."

                if rule not in seen:
                    seen.add(rule)
                    rules.append(rule)

            hypothesis["rules"] = rules

            normalized.append(hypothesis)

        return normalized