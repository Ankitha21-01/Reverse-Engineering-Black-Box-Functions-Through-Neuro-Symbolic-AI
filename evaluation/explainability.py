"""
=========================================================
Universal Explainability Engine
=========================================================

Produces a generic reasoning report for every execution.

=========================================================
"""


class Explainability:

    def __init__(self):
        pass

    # =====================================================

    def generate(

        self,

        hypothesis,

        execution,

        inference

    ):

        report = {}

        report["description"] = hypothesis.get(

            "description",

            ""

        )

        report["predicates"] = hypothesis.get(

            "predicates",

            []

        )

        report["rules"] = hypothesis.get(

            "rules",

            []

        )

        report["summary"] = inference.get(

            "summary",

            ""

        )

        report["trace"] = inference.get(

            "trace",

            []

        )

        report["status"] = execution.get(

            "status",

            "UNKNOWN"

        )

        return report

    # =====================================================

    def print(self, report):

        print("\n" + "=" * 60)

        print("EXPLAINABILITY REPORT")

        print("=" * 60)

        print("\nDescription")

        print(report["description"])

        print("\nPredicates")

        for p in report["predicates"]:

            print(" ", p)

        print("\nRules")

        for r in report["rules"]:

            print(" ", r)

        print("\nSummary")

        print(report["summary"])

        print("\nTrace")

        for t in report["trace"]:

            print(t)