"""
=========================================================
Universal Symbolic Executor
=========================================================

Executes verified symbolic hypotheses through the
Prolog Executor.

No algorithm-specific logic.

Responsibilities

• Validate hypothesis
• Delegate execution to SWI-Prolog
• Record symbolic reasoning trace
• Return unified execution result

=========================================================
"""


class SymbolicExecutor:

    def __init__(self, prolog_executor):

        self.prolog = prolog_executor

    # =====================================================

    def execute(

        self,

        hypothesis,

        input_data

    ):

        prolog_file = hypothesis.get("prolog_file")

        predicates = hypothesis.get(

            "predicates",

            []

        )

        rules = hypothesis.get(

            "rules",

            []

        )

        # -------------------------------------------------
        # Validate hypothesis
        # -------------------------------------------------

        if not prolog_file:

            return {

                "status": "ERROR",

                "result": None,

                "trace": [

                    {

                        "step": 1,

                        "action": "Locate Prolog program",

                        "status": "FAILED"

                    }

                ],

                "predicates": predicates,

                "rules": rules,

                "execution_time": 0.0

            }

        # -------------------------------------------------
        # Execute through Prolog
        # -------------------------------------------------

        execution = self.prolog.execute(

            prolog_file,

            input_data

        )

        # -------------------------------------------------
        # Build symbolic trace
        # -------------------------------------------------

        trace = []

        trace.append({

            "step": 1,

            "action": "Load symbolic program",

            "file": prolog_file,

            "status": "SUCCESS"

        })

        trace.append({

            "step": 2,

            "action": "Execute transform/2",

            "query": execution.get(

                "query",

                ""

            ),

            "status": execution.get(

                "status",

                "UNKNOWN"

            )

        })

        if execution.get("status") == "SUCCESS":

            trace.append({

                "step": 3,

                "action": "Collect variable bindings",

                "bindings": execution.get(

                    "bindings",

                    {}

                ),

                "status": "SUCCESS"

            })

        elif execution.get("status") == "NO_SOLUTION":

            trace.append({

                "step": 3,

                "action": "Search symbolic solution",

                "status": "NO_SOLUTION"

            })

        else:

            trace.append({

                "step": 3,

                "action": "Symbolic execution",

                "status": "FAILED",

                "error": execution.get(

                    "error",

                    ""

                )

            })

        # -------------------------------------------------
        # Unified result
        # -------------------------------------------------

        return {

            "status": execution.get(

                "status",

                "UNKNOWN"

            ),

            "input": input_data,

            "result": execution.get(

                "output"

            ),

            "bindings": execution.get(

                "bindings",

                {}

            ),

            "query": execution.get(

                "query",

                ""

            ),

            "trace": trace,

            "predicates": predicates,

            "rules": rules,

            "execution_time": execution.get(

                "execution_time",

                0.0

            )

        }

    # =====================================================

    def batch_execute(

        self,

        hypothesis,

        dataset

    ):

        outputs = []

        for sample in dataset:

            outputs.append(

                self.execute(

                    hypothesis,

                    sample

                )

            )

        return outputs