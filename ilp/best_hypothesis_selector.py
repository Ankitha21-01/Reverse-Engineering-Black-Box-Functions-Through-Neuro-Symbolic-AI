"""
=========================================================
Universal Best Hypothesis Selector
=========================================================

Selects the best learned hypothesis.

Selection Priority

1. Verified
2. Fully Executable
3. Average Accuracy
4. Evaluation Score
5. Ranking Score
6. Execution Success Rate
7. Coverage
8. Support
9. Confidence

=========================================================
"""


class BestHypothesisSelector:

    def __init__(self):
        pass

    # =====================================================

    def select(self, hypotheses):

        if not hypotheses:
            return None

        ranked = sorted(
            hypotheses,
            key=self.score,
            reverse=True
        )

        return ranked[0]

    # =====================================================

    def score(self, hypothesis):

        score = 0.0

        # --------------------------------------------------
        # Verification (Highest Priority)
        # --------------------------------------------------

        if hypothesis.get("verified", False):
            score += 2000

        if hypothesis.get("fully_executable", False):
            score += 1000

        elif hypothesis.get("executable", False):
            score += 500

        # --------------------------------------------------
        # Actual Learning Quality
        # --------------------------------------------------

        score += (
            float(
                hypothesis.get(
                    "average_accuracy",
                    0.0
                )
            ) * 1000
        )

        score += (
            float(
                hypothesis.get(
                    "evaluation_score",
                    0.0
                )
            ) * 700
        )

        score += (
            float(
                hypothesis.get(
                    "ranking_score",
                    0.0
                )
            )
        )

        score += (
            float(
                hypothesis.get(
                    "execution_success_rate",
                    0.0
                )
            ) * 300
        )

        score += (
            float(
                hypothesis.get(
                    "coverage",
                    0.0
                )
            ) * 200
        )

        score += (
            float(
                hypothesis.get(
                    "support",
                    0
                )
            ) * 100
        )

        # --------------------------------------------------
        # Structural Quality
        # --------------------------------------------------

        score += len(
            hypothesis.get(
                "predicates",
                []
            )
        )

        score += (
            len(
                hypothesis.get(
                    "rules",
                    []
                )
            ) * 2
        )

        # --------------------------------------------------
        # LLM Confidence (Lowest Priority)
        # --------------------------------------------------

        score += (
            float(
                hypothesis.get(
                    "confidence",
                    0.0
                )
            ) * 5
        )

        return round(score, 3)

    # =====================================================

    def rank(self, hypotheses):

        return sorted(
            hypotheses,
            key=self.score,
            reverse=True
        )

    # =====================================================

    def explain(self, hypothesis):

        print()
        print("=" * 60)
        print("BEST HYPOTHESIS")
        print("=" * 60)
        print()

        print("Description :", hypothesis.get("description", ""))

        print("Score :", self.score(hypothesis))

        print("Verified :", hypothesis.get("verified", False))

        print("Executable :", hypothesis.get("fully_executable", False))

        print("Average Accuracy :", hypothesis.get("average_accuracy", 0))

        print("Evaluation Score :", hypothesis.get("evaluation_score", 0))

        print("Execution Success :", hypothesis.get("execution_success_rate", 0))

        print("Ranking Score :", hypothesis.get("ranking_score", 0))

        print("Support :", hypothesis.get("support", 0))

        print("Coverage :", hypothesis.get("coverage", 0))

        print("Confidence :", hypothesis.get("confidence", 0))