"""
=========================================================
Universal Reasoning Engine
=========================================================

Generates reasoning from actual symbolic evaluation.

Uses

✓ Average Accuracy
✓ Execution Success Rate
✓ Support
✓ Coverage
✓ Evaluation Score
✓ Verification
✓ Executability
✓ Ranking Score

No algorithm-specific assumptions.

=========================================================
"""


class ReasoningEngine:

    def __init__(self):
        pass

    # =====================================================

    def explain(self, hypotheses):

        explanations = []

        for hypothesis in hypotheses:

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

            support = int(
                hypothesis.get(
                    "support",
                    0
                )
            )

            coverage = float(
                hypothesis.get(
                    "coverage",
                    0.0
                )
            )

            evaluation_score = float(
                hypothesis.get(
                    "evaluation_score",
                    0.0
                )
            )

            ranking_score = float(
                hypothesis.get(
                    "ranking_score",
                    0.0
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

            lines = []

            lines.append(
                f"Hypothesis : {hypothesis.get('description', 'Unknown')}"
            )

            lines.append(
                f"Predicates learned : {len(hypothesis.get('predicates', []))}"
            )

            lines.append(
                f"Rules generated : {len(hypothesis.get('rules', []))}"
            )

            lines.append(
                f"Support : {support}"
            )

            lines.append(
                f"Coverage : {coverage:.2f}"
            )

            lines.append(
                f"Average Accuracy : {average_accuracy:.2f}"
            )

            lines.append(
                f"Execution Success Rate : {execution_success_rate:.2f}"
            )

            lines.append(
                f"Evaluation Score : {evaluation_score:.2f}"
            )

            lines.append(
                f"Ranking Score : {ranking_score:.2f}"
            )

            # -----------------------------------------
            # Execution status
            # -----------------------------------------

            if executable:

                lines.append(
                    "Executable symbolic program generated."
                )

            else:

                lines.append(
                    "Program is not yet fully executable."
                )

            # -----------------------------------------
            # Verification
            # -----------------------------------------

            if verified:

                lines.append(
                    "Logical verification passed."
                )

            else:

                lines.append(
                    "Logical verification failed."
                )

            # -----------------------------------------
            # Final reasoning
            # -----------------------------------------

            if verified and executable:

                lines.append(
                    "Hypothesis satisfies symbolic verification and is ready for execution."
                )

            elif executable:

                lines.append(
                    "Program executes successfully but requires further verification."
                )

            else:

                lines.append(
                    "Hypothesis requires further learning before symbolic execution."
                )

            explanations.append({

                "description":
                    hypothesis.get(
                        "description",
                        ""
                    ),

                "verified":
                    verified,

                "ranking_score":
                    ranking_score,

                "reasoning":
                    lines,

                "explanation":
                    "\n".join(lines)

            })

        return explanations