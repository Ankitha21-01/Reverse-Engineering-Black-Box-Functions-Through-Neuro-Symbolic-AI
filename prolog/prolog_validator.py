"""
=========================================================
Universal Prolog Validator
=========================================================

Lightweight validation for generated Prolog programs.

Checks

✓ duplicate removal
✓ syntax
✓ transform/2 exists

Does NOT reject recursive clauses.

=========================================================
"""


class PrologValidator:

    def validate(self, hypothesis):

        executable = []
        invalid = []

        seen = set()

        transform_found = False

        for rule in hypothesis.get("rules", []):

            rule = str(rule).strip()

            if not rule:
                continue

            if not rule.endswith("."):
                rule += "."

            if rule in seen:
                continue

            seen.add(rule)

            if self.is_valid(rule):

                executable.append(rule)

                if rule.startswith("transform("):
                    transform_found = True

            else:

                invalid.append(rule)

        hypothesis["rules"] = executable

        hypothesis["invalid_rules"] = invalid

        hypothesis["executable_rules"] = executable

        hypothesis["total_rules"] = len(executable)

        hypothesis["fully_executable"] = (

            transform_found and
            len(executable) > 0

        )

        return hypothesis

    # --------------------------------------------------

    def is_valid(self, rule):

        if not rule:
            return False

        if not rule.endswith("."):
            return False

        if "(" not in rule or ")" not in rule:
            return False

        return True