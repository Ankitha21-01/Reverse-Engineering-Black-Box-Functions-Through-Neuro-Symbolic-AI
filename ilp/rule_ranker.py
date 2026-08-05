"""
=========================================================
Universal Rule Ranker
=========================================================

Ranks symbolic hypotheses.

Ranking Priority

1. Average Accuracy
2. Evaluation Score
3. Coverage
4. Execution Success
5. Support
6. Verification
7. Program Completeness
8. Predicate Richness
9. Rule Richness
10. Confidence (least important)

=========================================================
"""


class RuleRanker:

    def __init__(self):
        pass

    # =====================================================

    def rank(self, hypotheses):

        for hypothesis in hypotheses:

            confidence = float(
                hypothesis.get("confidence", 0.0)
            )

            coverage = float(
                hypothesis.get("coverage", 0.0)
            )

            support = int(
                hypothesis.get("support", 0)
            )

            average_accuracy = float(
                hypothesis.get("average_accuracy", 0.0)
            )

            execution_success_rate = float(
                hypothesis.get("execution_success_rate", 0.0)
            )

            evaluation_score = float(
                hypothesis.get("evaluation_score", 0.0)
            )

            predicate_count = int(
                hypothesis.get("predicate_count", 0)
            )

            rule_count = int(
                hypothesis.get("rule_count", 0)
            )

            helper_rules = int(
                hypothesis.get("helper_rule_count", 0)
            )

            transform_rules = int(
                hypothesis.get("transform_rule_count", 0)
            )

            executable = bool(
                hypothesis.get("executable", False)
            )

            verified = bool(
                hypothesis.get("verified", False)
            )

            execution_ready = bool(
                hypothesis.get("execution_ready", False)
            )

            fully_executable = bool(
                hypothesis.get("fully_executable", False)
            )

            score = 0.0

            # -------------------------------------------------
            # Actual learning quality (Highest Priority)
            # -------------------------------------------------

            score += average_accuracy * 1000

            score += evaluation_score * 600

            score += coverage * 300

            score += execution_success_rate * 250

            score += support * 100

            # -------------------------------------------------
            # Program completeness
            # -------------------------------------------------

            if transform_rules > 0:
                score += 40

            if helper_rules > 0:
                score += 20

            if executable:
                score += 50

            if verified:
                score += 75

            if execution_ready:
                score += 75

            if fully_executable:
                score += 100

            # -------------------------------------------------
            # Structural richness
            # -------------------------------------------------

            score += min(predicate_count, 25)

            score += min(rule_count, 25)

            # -------------------------------------------------
            # Confidence (very small influence)
            # -------------------------------------------------

            score += confidence * 5

            hypothesis["ranking_score"] = round(score, 3)

        hypotheses.sort(

            key=lambda h: (

                h.get("average_accuracy", 0),

                h.get("evaluation_score", 0),

                h.get("coverage", 0),

                h.get("execution_success_rate", 0),

                h.get("support", 0),

                h.get("verified", False),

                h.get("fully_executable", False),

                h.get("execution_ready", False),

                h.get("ranking_score", 0)

            ),

            reverse=True

        )

        return hypotheses