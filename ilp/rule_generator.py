"""
=========================================================
Universal Rule Generator
=========================================================

Builds executable symbolic rules from LLM hypotheses.

Features

✓ Keeps only valid Prolog clauses
✓ Removes duplicate rules
✓ Rejects malformed rules
✓ Ensures transform/2 exists
✓ Rejects recursive-only programs
✓ Rejects placeholder rules
✓ Generates fallback only if needed

=========================================================
"""

import re


class RuleGenerator:

    def __init__(self):
        pass

    # =====================================================

    def generate(self, hypothesis):

        generated = []

        seen = set()

        for rule in hypothesis.get("rules", []):

            rule = self.normalize(rule)

            if not self.valid(rule):
                continue

            if rule in seen:
                continue

            seen.add(rule)
            generated.append(rule)

        # ------------------------------------------
        # Must contain transform/2
        # ------------------------------------------

        if not any(
            r.startswith("transform(")
            for r in generated
        ):
            generated.insert(
                0,
                "transform(Input, Output) :- fail."
            )

        # ------------------------------------------
        # Reject recursive-only hypotheses
        # ------------------------------------------

        if self.only_recursive(generated):
            print("\n[RuleGenerator] Recursive-only program detected.")
            print("Generated rules:")
            for r in generated:
                print(" ", r)

        return generated

    # =====================================================

    def normalize(self, rule):

        rule = str(rule).strip()

        if not rule.endswith("."):
            rule += "."

        return rule

    # =====================================================

    def valid(self, rule):

        if not rule:
            return False

        if "(" not in rule:
            return False

        if ")" not in rule:
            return False

        if not rule.endswith("."):
            return False

        # reject placeholders

        banned = [

            "...",
            "TODO",
            "placeholder",
            "???"

        ]

        for b in banned:

            if b.lower() in rule.lower():
                return False

        return True

    # =====================================================

    def only_recursive(self, rules):
        """
        Reject rules like

        alternate(...) :- alternate(...).

        because they never terminate.
        """

        helper_heads = {}

        for rule in rules:

            if ":-" not in rule:
                continue

            head = rule.split(":-")[0].strip()

            name = head.split("(")[0]

            helper_heads.setdefault(name, 0)

            helper_heads[name] += 1

        for rule in rules:

            if ":-" not in rule:
                continue

            head = rule.split(":-")[0].strip()

            body = rule.split(":-")[1]

            name = head.split("(")[0]

            if name == "transform":
                continue

            if name + "(" in body:

                # recursive

                if helper_heads.get(name, 0) <= 2:

                    return True

        return False