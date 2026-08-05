"""
=========================================================
Universal Inference Engine
=========================================================

Performs symbolic inference over actual Prolog execution.

No algorithm-specific assumptions.

Works for any learned symbolic rule.

=========================================================
"""


class InferenceEngine:

    def __init__(self):
        pass

    # =====================================================

    def infer(self, execution_result):

        status = execution_result.get("status", "UNKNOWN")

        query = execution_result.get("query", "")

        output = execution_result.get("output", None)

        bindings = execution_result.get("bindings", {})

        execution_time = execution_result.get(
            "execution_time",
            0.0
        )

        input_data = execution_result.get("input", None)

        error = execution_result.get("error", None)

        summary = self.build_summary(

            status,
            query,
            bindings,
            error

        )

        details = {

            "status": status,

            "query": query,

            "execution_time": execution_time,

            "binding_count": len(bindings),

            "input_type": type(input_data).__name__,

            "output_type": type(output).__name__,

            "output": output,

            "error": error

        }

        return {

            "summary": summary,

            "details": details,

            "bindings": bindings

        }

    # =====================================================

    def build_summary(

        self,

        status,

        query,

        bindings,

        error=None

    ):

        lines = []

        lines.append(f"Execution Status : {status}")

        if query:
            lines.append(f"Executed Query : {query}")

        lines.append(
            f"Variable Bindings : {len(bindings)}"
        )

        if status == "SUCCESS":

            lines.append(
                "Symbolic reasoning completed successfully."
            )

        elif status == "NO_SOLUTION":

            lines.append(
                "No symbolic solution satisfied the learned rules."
            )

        else:

            lines.append(
                "Symbolic execution terminated with an error."
            )

            if error:
                lines.append(f"Reason : {error}")

        return "\n".join(lines)

    # =====================================================

    def explain(self, inference):

        print()

        print("=" * 60)
        print("INFERENCE SUMMARY")
        print("=" * 60)

        print(inference["summary"])

        print()

        print("=" * 60)
        print("DETAILS")
        print("=" * 60)

        for key, value in inference["details"].items():

            print(f"{key:20}: {value}")

        bindings = inference.get("bindings", {})

        if bindings:

            print()

            print("=" * 60)
            print("VARIABLE BINDINGS")
            print("=" * 60)

            for variable, value in bindings.items():

                print(f"{variable:15}: {value}")