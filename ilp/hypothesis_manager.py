"""
=========================================================
Universal Hypothesis Manager
=========================================================

Processes hypotheses before ILP learning.

Responsibilities

✓ Validation
✓ Rule normalization
✓ Duplicate removal
✓ Confidence normalization
✓ Predicate counting
✓ Rule counting
✓ Basic quality filtering

Executability and verification are handled later.

=========================================================
"""


class HypothesisManager:

    def __init__(self):
        pass

    # ----------------------------------------------------

    def _normalize_rule(self, rule):

        rule = str(rule).strip()

        if not rule:
            return None

        if not rule.endswith("."):
            rule += "."

        return rule

    # ----------------------------------------------------

    def _looks_like_identity(self, rules):

        suspicious = [

            "Output=Input",
            "Output = Input",
            "Input=Output",
            "Input = Output",

            "transform(Input,Input)",
            "transform(X,X)",

        ]

        joined = " ".join(rules)

        for pattern in suspicious:
            if pattern in joined:
                return True

        return False

    # ----------------------------------------------------

    def process(self, llm_result):

        hypotheses = llm_result.get("hypotheses", [])

        processed = []

        seen_programs = set()

        seen_descriptions = set()

        for hypothesis in hypotheses:

            description = str(
                hypothesis.get("description", "")
            ).strip()

            if not description:
                continue

            # --------------------------------------------
            # Remove duplicate descriptions
            # --------------------------------------------

            if description.lower() in seen_descriptions:
                continue

            seen_descriptions.add(description.lower())

            # --------------------------------------------
            # Predicates
            # --------------------------------------------

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

            # --------------------------------------------
            # Normalize Rules
            # --------------------------------------------

            rules = []

            transform_rules = 0
            helper_rules = 0

            for rule in hypothesis.get("rules", []):

                rule = self._normalize_rule(rule)

                if rule is None:
                    continue

                if rule in rules:
                    continue

                rules.append(rule)

                head = rule.split(":-")[0].strip()

                if head.startswith("transform("):
                    transform_rules += 1
                else:
                    helper_rules += 1

            # --------------------------------------------
            # Remove duplicate programs
            # --------------------------------------------

            signature = tuple(rules)

            if signature in seen_programs:
                continue

            seen_programs.add(signature)

            # --------------------------------------------
            # Confidence
            # --------------------------------------------

            try:
                confidence = float(
                    hypothesis.get("confidence", 0.0)
                )
            except Exception:
                confidence = 0.0

            confidence = max(0.0, min(confidence, 1.0))

            # --------------------------------------------
            # Penalize suspicious programs
            # --------------------------------------------

            if self._looks_like_identity(rules):
                confidence *= 0.25

            if helper_rules == 0:
                confidence *= 0.60

            if len(rules) < 2:
                confidence *= 0.50

            # --------------------------------------------
            # Validation
            # --------------------------------------------

            valid = (

                len(rules) > 0

                and transform_rules == 1

                and len(predicates) > 0

            )

            processed.append({

                "description": description,

                "confidence": round(confidence, 3),

                "predicates": predicates,

                "rules": rules,

                "predicate_count": len(predicates),

                "rule_count": len(rules),

                "transform_rule_count": transform_rules,

                "helper_rule_count": helper_rules,

                "valid": valid,

                # Filled later

                "verified": False,

                "execution_ready": False,

                "fully_executable": False,

                "coverage": 0.0,

                "support": 0,

                "evaluation_score": 0.0

            })

        # --------------------------------------------
        # Sort better hypotheses first
        # --------------------------------------------

        processed.sort(

            key=lambda h: (

                h["valid"],

                h["confidence"],

                h["helper_rule_count"],

                h["rule_count"]

            ),

            reverse=True

        )

        return processed