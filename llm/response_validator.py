"""
=========================================================
Universal Response Validator
=========================================================

Validates and normalizes LLM JSON responses.

Responsibilities

✓ Validate overall JSON structure
✓ Remove duplicate hypotheses
✓ Normalize predicates
✓ Normalize rules
✓ Normalize confidence
✓ Ensure transform/2 exists
✓ Ensure helper predicates exist
✓ Reject malformed hypotheses
✓ Rank hypotheses

=========================================================
"""

import re


class ResponseValidator:

    def __init__(self):

        self.required_fields = [

            "problem_type",
            "reasoning",
            "hypotheses"

        ]

        self.builtins = {

            "append",
            "member",
            "reverse",
            "length",
            "sort",
            "msort",
            "findall",
            "bagof",
            "setof",
            "nth0",
            "integer",
            "number",
            "atom",
            "atomic",
            "var",
            "nonvar",
            "is",
            "=",
            "\\=",
            ">",
            "<",
            ">=",
            "=<"

        }

    # =====================================================

    def validate(self, response):

        if not isinstance(response, dict):
            return self.empty_response()

        for field in self.required_fields:

            if field not in response:

                if field == "hypotheses":
                    response[field] = []
                else:
                    response[field] = ""

        response["problem_type"] = str(
            response.get("problem_type", "Unknown")
        )

        response["reasoning"] = str(
            response.get("reasoning", "")
        )

        response["hypotheses"] = self.validate_hypotheses(
            response.get("hypotheses", [])
        )

        return response

    # =====================================================

    def validate_hypotheses(self, hypotheses):

        validated = []

        seen = set()

        if not isinstance(hypotheses, list):
            return validated

        for index, hypothesis in enumerate(hypotheses):

            if not isinstance(hypothesis, dict):
                continue

            description = str(
                hypothesis.get("description", "")
            ).strip()

            if not description:
                continue

            predicates = self.clean_list(
                hypothesis.get("predicates", [])
            )

            rules = self.normalize_rules(
                hypothesis.get("rules", [])
            )

            confidence = self.normalize_confidence(
                hypothesis.get("confidence", 0.0)
            )

            if not rules:
                continue

            if not self.has_transform(rules):
                continue

            if not self.helper_predicates_defined(rules):
                continue

            signature = (

                tuple(predicates),
                tuple(rules)

            )

            if signature in seen:
                continue

            seen.add(signature)

            hypothesis_score = (

                confidence * 100

                + len(rules)

                + len(predicates)

            )

            validated.append({

                "id": hypothesis.get(
                    "id",
                    index + 1
                ),

                "description": description,

                "predicates": predicates,

                "rules": rules,

                "confidence": confidence,

                "predicate_count": len(predicates),

                "rule_count": len(rules),

                "validation_score": round(
                    hypothesis_score,
                    3
                )

            })

        validated.sort(

            key=lambda h: (

                h["validation_score"],

                h["confidence"]

            ),

            reverse=True

        )

        return validated
        # =====================================================

    def normalize_rules(self, rules):

        normalized = []

        seen = set()

        if not isinstance(rules, list):
            return normalized

        for rule in rules:

            rule = str(rule).strip()

            if not rule:
                continue

            if not rule.endswith("."):
                rule += "."

            if rule in seen:
                continue

            seen.add(rule)

            normalized.append(rule)

        return normalized

    # =====================================================

    def clean_list(self, values):

        cleaned = []

        seen = set()

        if not isinstance(values, list):
            return cleaned

        for value in values:

            value = str(value).strip()

            if not value:
                continue

            if value in seen:
                continue

            seen.add(value)

            cleaned.append(value)

        cleaned.sort()

        return cleaned

    # =====================================================

    def normalize_confidence(self, confidence):

        try:
            confidence = float(confidence)

        except Exception:
            confidence = 0.0

        confidence = max(0.0, min(1.0, confidence))

        return round(confidence, 3)

    # =====================================================

    def has_transform(self, rules):

        transform_rules = 0

        for rule in rules:

            head = rule.split(":-")[0].strip()

            if head.startswith("transform("):
                transform_rules += 1

        return transform_rules == 1

    # =====================================================

    def helper_predicates_defined(self, rules):

        called = self.extract_called_predicates(rules)

        defined = self.extract_defined_predicates(rules)

        for predicate in called:

            if predicate == "transform":
                continue

            if predicate in self.builtins:
                continue

            if predicate not in defined:
                return False

        return True

    # =====================================================

    def extract_called_predicates(self, rules):

        called = set()

        pattern = r'([a-z][A-Za-z0-9_]*)\s*\('

        for rule in rules:

            if ":-" not in rule:
                continue

            body = rule.split(":-", 1)[1]

            matches = re.findall(pattern, body)

            for match in matches:

                called.add(match)

        return called

    # =====================================================

    def extract_defined_predicates(self, rules):

        defined = set()

        pattern = r'^([a-z][A-Za-z0-9_]*)\s*\('

        for rule in rules:

            head = rule.split(":-")[0].strip()

            match = re.match(pattern, head)

            if match:

                defined.add(match.group(1))

        return defined

    # =====================================================

    def empty_response(self):

        return {

            "problem_type": "Unknown",

            "reasoning": "",

            "hypotheses": []

        }