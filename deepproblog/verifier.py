"""
=========================================================
Universal DeepProbLog Verifier
=========================================================

Verifies symbolic hypotheses.

Checks

✓ transform/2 exists
✓ Helper predicates are defined
✓ Complete executable program
✓ Execution readiness
✓ Average accuracy
✓ Evaluation score

=========================================================
"""

import re


class DeepProbLogVerifier:

        def __init__(self):

            self.builtins = {

                "append",
                "member",
                "length",
                "reverse",
                "sort",
                "msort",
                "select",
                "nth0",
                "integer",
                "number",
                "atom",
                "is",
                "true",
                "fail"

            }

            self.minimum_accuracy = 0.80
            self.minimum_execution = 0.90
            self.minimum_score = 0.70

             # =====================================================

        def defined_predicates(self, rules):

            defined = set()

            transform_exists = False

            for rule in rules:

                rule = str(rule).strip()

                if not rule:
                    continue

                head = rule.split(":-")[0].strip()

                match = re.match(

                    r"([a-zA-Z_][A-Za-z0-9_]*)\(",

                    head

                )

                if match:

                    predicate = match.group(1)

                    defined.add(predicate)

                    if predicate == "transform":

                        transform_exists = True

            return defined, transform_exists


    # =====================================================

        def called_predicates(self, rules):

            called = set()

            for rule in rules:

                if ":-" not in rule:

                    continue

                body = rule.split(":-",1)[1]

                names = re.findall(

                    r"([a-zA-Z_][A-Za-z0-9_]*)\(",

                    body

                )

                for name in names:

                    if name not in self.builtins:

                        called.add(name)

            return called


    # =====================================================

        def coverage_score(

            self,

            defined,

            called

        ):

            if len(called) == 0:

                return 1.0

            covered = len(

                called & defined

            )

            return round(

                covered / len(called),

                3

            )


    # =====================================================

        def dead_predicates(

            self,

            defined,

            called

        ):

            return sorted(

                p

                for p in defined

                if p != "transform"

                and p not in called

            )


    # =====================================================

        def recursive_predicates(

            self,

            rules

        ):

            recursive = []

            for rule in rules:

                if ":-" not in rule:

                    continue

                head = rule.split(":-")[0]

                body = rule.split(":-")[1]

                match = re.match(

                    r"([a-zA-Z_][A-Za-z0-9_]*)\(",

                    head

                )

                if not match:

                    continue

                predicate = match.group(1)

                if predicate + "(" in body:

                    recursive.append(predicate)

            return sorted(

                set(recursive)

            )   
    # =====================================================

           # =====================================================

        def verify(self, hypotheses):

            verified = []

            for hypothesis in hypotheses:

                rules = hypothesis.get("rules", [])

                defined, transform_exists = self.defined_predicates(rules)

                called = self.called_predicates(rules)

                missing = sorted(

                    called - defined

                )

                dead = self.dead_predicates(

                    defined,

                    called

                )

                recursive = self.recursive_predicates(

                    rules

                )

                coverage = self.coverage_score(

                    defined,

                    called

                )

                average_accuracy = float(

                    hypothesis.get(

                        "average_accuracy",

                        0.0

                    )

                )

                execution_success_rate = float(

                    hypothesis.get(

                        "execution_success_rate",

                        0.0

                    )

                )

                evaluation_score = float(

                    hypothesis.get(

                        "evaluation_score",

                        0.0

                    )

                )

                execution_score = float(

                    hypothesis.get(

                        "average_execution_score",

                        hypothesis.get(

                            "execution_score",

                            0.0

                        )

                    )

                )

                executable = bool(

                    hypothesis.get(

                        "fully_executable",

                        False

                    )

                )

                execution_ready = bool(

                    hypothesis.get(

                        "execution_ready",

                        False

                    )

                )

                complete_program = (

                    transform_exists

                    and

                    len(missing) == 0

                )

                verification_score = round(

                    (

                        average_accuracy * 0.30

                        +

                        execution_success_rate * 0.20

                        +

                        evaluation_score * 0.20

                        +

                        execution_score * 0.20

                        +

                        coverage * 0.10

                    ),

                    3

                )

                verified_flag = (

                    complete_program

                    and executable

                    and execution_ready

                    and average_accuracy >= self.minimum_accuracy

                    and execution_success_rate >= self.minimum_execution

                    and evaluation_score >= self.minimum_score

                    and coverage >= 1.0

                )

                hypothesis = dict(hypothesis)

                hypothesis["transform_exists"] = transform_exists

                hypothesis["defined_predicates"] = sorted(defined)

                hypothesis["called_predicates"] = sorted(called)

                hypothesis["missing_predicates"] = missing

                hypothesis["dead_predicates"] = dead

                hypothesis["recursive_predicates"] = recursive

                hypothesis["coverage_score"] = coverage

                hypothesis["complete_program"] = complete_program

                hypothesis["verification_score"] = verification_score

                hypothesis["verified"] = verified_flag

                hypothesis["verification_report"] = {

                    "complete_program": complete_program,

                    "transform_exists": transform_exists,

                    "coverage": coverage,

                    "missing": len(missing),

                    "dead": len(dead),

                    "recursive": len(recursive),

                    "accuracy": average_accuracy,

                    "execution_rate": execution_success_rate,

                    "execution_score": execution_score,

                    "evaluation_score": evaluation_score,

                    "verified": verified_flag

                }

                verified.append(hypothesis)

            verified.sort(

                key=lambda h: (

                    h["verified"],

                    h["verification_score"]

                ),

                reverse=True

            )

            return verified