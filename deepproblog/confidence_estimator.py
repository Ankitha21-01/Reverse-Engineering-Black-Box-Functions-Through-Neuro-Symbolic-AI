"""
=========================================================
Universal Confidence Estimator
=========================================================

Estimates confidence of symbolic hypotheses using
actual execution performance.

Confidence is computed from

✓ Average Accuracy
✓ Evaluation Score
✓ Execution Success Rate
✓ Coverage
✓ Verification
✓ Executability

LLM confidence has very little influence.

=========================================================
"""


class ConfidenceEstimator:

    def __init__(self):
        pass

    # =====================================================

    def estimate(self, hypotheses):

        scores = []

        for hypothesis in hypotheses:

            average_accuracy = float(
                hypothesis.get(
                    "average_accuracy",
                    0.0
                )
            )

            evaluation_score = float(
                hypothesis.get(
                    "evaluation_score",
                    0.0
                )
            )

            execution_success_rate = float(
                hypothesis.get(
                    "execution_success_rate",
                    0.0
                )
            )

            coverage = float(
                hypothesis.get(
                    "coverage",
                    0.0
                )
            )

            support = int(
                hypothesis.get(
                    "support",
                    0
                )
            )

            executable = bool(
                hypothesis.get(
                    "fully_executable",
                    False
                )
            )

            verified = bool(
                hypothesis.get(
                    "verified",
                    False
                )
            )

            llm_confidence = float(
                hypothesis.get(
                    "confidence",
                    0.0
                )
            )

            # -------------------------------------------------
            # Confidence Computation
            # -------------------------------------------------

            score = (

                average_accuracy * 0.40 +

                evaluation_score * 0.30 +

                execution_success_rate * 0.15 +

                coverage * 0.10 +

                llm_confidence * 0.05

            )

            # -------------------------------------------------
            # Bonus for executable program
            # -------------------------------------------------

            if executable:
                score += 0.05

            if verified:
                score += 0.05

            score = min(score, 1.0)

            scores.append({

                "score": round(score, 4),

                "average_accuracy": round(
                    average_accuracy,
                    4
                ),

                "evaluation_score": round(
                    evaluation_score,
                    4
                ),

                "execution_success_rate": round(
                    execution_success_rate,
                    4
                ),

                "coverage": round(
                    coverage,
                    4
                ),

                "support": support,

                "verified": verified,

                "executable": executable

            })

        return scores