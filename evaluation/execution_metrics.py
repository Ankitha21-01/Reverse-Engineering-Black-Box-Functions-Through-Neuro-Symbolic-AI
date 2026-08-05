"""
=========================================================
Universal Execution Metrics
=========================================================

Computes generic metrics from symbolic execution.

No algorithm-specific assumptions.

=========================================================
"""


class ExecutionMetrics:

    def __init__(self):
        pass

    # =====================================================

    def evaluate(self, execution_result):

        bindings = execution_result.get(
            "bindings",
            {}
        )

        trace = execution_result.get(
            "trace",
            []
        )

        output = execution_result.get(
            "result",
            execution_result.get("output")
        )

        status = execution_result.get(
            "status",
            "UNKNOWN"
        )

        metrics = {

            "status":
                status,

            "execution_time":
                execution_result.get(
                    "execution_time",
                    0.0
                ),

            "query":
                execution_result.get(
                    "query",
                    ""
                ),

            "binding_count":
                len(bindings),

            "trace_steps":
                len(trace),

            "rule_count":
                len(
                    execution_result.get(
                        "rules",
                        []
                    )
                ),

            "predicate_count":
                len(
                    execution_result.get(
                        "predicates",
                        []
                    )
                ),

            "output_generated":
                output is not None,

            "input_type":
                type(
                    execution_result.get(
                        "input"
                    )
                ).__name__,

            "output_type":
                type(
                    output
                ).__name__,

            "success":
                status == "SUCCESS"

        }

        return metrics

    # =====================================================

    def compare(

        self,

        expected,

        predicted

    ):

        comparison = {

            "exact_match":
                expected == predicted,

            "expected_type":
                type(expected).__name__,

            "predicted_type":
                type(predicted).__name__,

            "expected":
                expected,

            "predicted":
                predicted

        }

        return comparison

    # =====================================================

    def print_report(

        self,

        metrics

    ):

        print()

        print("=" * 60)

        print("EXECUTION METRICS")

        print("=" * 60)

        for key, value in metrics.items():

            print(f"{key:20}: {value}")

        print("=" * 60)