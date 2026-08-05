"""
=========================================================
Executable Rule Generator
=========================================================

Converts ranked hypotheses into executable symbolic rules.

Responsibilities

✓ Normalize Prolog rules
✓ Remove duplicates
✓ Ensure transform/2 exists
✓ Preserve helper predicates
✓ Prepare hypotheses for verification

Actual executability is determined by the
DeepProbLogVerifier.

=========================================================
"""


class ExecutableRuleGenerator:

    def __init__(self):
        pass

    # =====================================================

    def generate(self, hypotheses):

        executable = []

        for hypothesis in hypotheses:

            executable_rules = []
            seen = set()

            transform_rules = 0

            # ----------------------------------------------
            # Normalize rules
            # ----------------------------------------------

            for rule in hypothesis.get("rules", []):

                rule = str(rule).strip()

                if not rule:
                    continue

                if not rule.endswith("."):
                    rule += "."

                # Ignore malformed rules
                if "(" not in rule or ")" not in rule:
                    continue

                # Remove duplicates
                if rule in seen:
                    continue

                seen.add(rule)
                executable_rules.append(rule)

                if rule.startswith("transform("):
                    transform_rules += 1

            # ----------------------------------------------
            # Build new hypothesis
            # ----------------------------------------------

            new_hypothesis = dict(hypothesis)

            new_hypothesis["executable_rules"] = executable_rules

            new_hypothesis["total_rules"] = len(executable_rules)

            # A program is complete if it contains transform/2
            new_hypothesis["fully_executable"] = (
                transform_rules >= 1
                and len(executable_rules) > 0
            )

            # Final readiness depends on verifier results
            new_hypothesis["execution_ready"] = (
                new_hypothesis["fully_executable"]
                and hypothesis.get("verified", False)
                and len(hypothesis.get("missing_predicates", [])) == 0
            )

            executable.append(new_hypothesis)

        return executable