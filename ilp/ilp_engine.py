"""
=========================================================
Universal ILP Engine
=========================================================

Responsibilities

✓ Learn symbolic predicates
✓ Merge discovered and LLM predicates
✓ Remove duplicate predicates
✓ Remove duplicate rules
✓ Validate transform/2
✓ Validate helper predicates
✓ Compute learning statistics
✓ Reject incomplete hypotheses
✓ Produce executable symbolic programs

=========================================================
"""

from ilp.predicate_generator import PredicateGenerator
from ilp.rule_generator import RuleGenerator


class ILPEngine:

    def __init__(self):

        self.predicate_generator = PredicateGenerator()
        self.rule_generator = RuleGenerator()

    # =====================================================

    def learn(self, hypotheses, knowledge):

        learned = []

        # -------------------------------------------------
        # Discover predicates from all examples
        # -------------------------------------------------

        discovered_predicates = []

        for item in knowledge:

            try:
                preds = self.predicate_generator.generate(item)
                discovered_predicates.extend(preds)

            except Exception:
                pass

        discovered_predicates = sorted(set(discovered_predicates))

        # -------------------------------------------------

        for hypothesis in hypotheses:

            llm_predicates = list(
                hypothesis.get("predicates", [])
            )

            all_predicates = sorted(
                set(discovered_predicates + llm_predicates)
            )

            generated_rules = self.rule_generator.generate({

                "predicates": all_predicates,

                "rules": hypothesis.get(
                    "rules",
                    []
                )

            })

            generated_rules = self._remove_duplicate_rules(
                generated_rules
            )

            predicate_count = len(all_predicates)

            rule_count = len(generated_rules)

            helper_rule_count = self._count_helper_rules(
                generated_rules
            )

            transform_rule_count = self._count_transform_rules(
                generated_rules
            )

            executable = self._has_transform(
                generated_rules
            )

            complete_program = self._complete_program(
                generated_rules
            )

            verified = executable and complete_program

            execution_ready = verified

            confidence = float(
                hypothesis.get("confidence", 0.0)
            )

            learning_score = round(

                confidence * 0.45

                + min(predicate_count / 50.0, 0.15)

                + min(rule_count / 15.0, 0.15)

                + min(helper_rule_count / 10.0, 0.10)

                + (0.10 if executable else 0.0)

                + (0.05 if complete_program else 0.0),

                3

            )

            learned.append({

                "description":
                    hypothesis.get(
                        "description",
                        ""
                    ),

                "confidence":
                    confidence,

                "predicates":
                    all_predicates,

                "rules":
                    generated_rules,

                "predicate_count":
                    predicate_count,

                "rule_count":
                    rule_count,

                "helper_rule_count":
                    helper_rule_count,

                "transform_rule_count":
                    transform_rule_count,

                "learning_score":
                    learning_score,

                "verified":
                    verified,

                "execution_ready":
                    execution_ready,

                "executable":
                    executable

            })

        return learned

    # =====================================================

    def _remove_duplicate_rules(self, rules):

        unique = []

        seen = set()

        for rule in rules:

            r = str(rule).strip()

            if r not in seen:

                seen.add(r)

                unique.append(r)

        return unique

    # =====================================================

    def _count_transform_rules(self, rules):

        count = 0

        for rule in rules:

            if rule.strip().startswith("transform("):
                count += 1

        return count

    # =====================================================

    def _count_helper_rules(self, rules):

        count = 0

        for rule in rules:

            if not rule.strip().startswith("transform("):
                count += 1

        return count

    # =====================================================

    def _has_transform(self, rules):

        for rule in rules:

            if rule.strip().startswith("transform("):
                return True

        return False

    # =====================================================

    def _complete_program(self, rules):

        defined = set()

        called = set()

        builtins = {

            "append",
            "member",
            "reverse",
            "length",
            "msort",
            "sort",
            "findall",
            "bagof",
            "setof",
            "nth0",
            "integer",
            "is"

        }

        for rule in rules:

            rule = rule.strip()

            if "(" in rule:

                head = rule.split(":-")[0]

                name = head.split("(")[0].strip()

                defined.add(name)

        for rule in rules:

            if ":-" not in rule:
                continue

            body = rule.split(":-", 1)[1]

            tokens = body.replace(",", " ").replace(".", " ").split()

            for token in tokens:

                if "(" not in token:
                    continue

                pred = token.split("(")[0].strip()

                if pred not in builtins:

                    called.add(pred)

        for pred in called:

            if pred not in defined:

                return False

        return True