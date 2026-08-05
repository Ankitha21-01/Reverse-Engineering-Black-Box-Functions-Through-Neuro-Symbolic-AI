"""
=========================================================
Universal Execution Engine
=========================================================

Responsible for executing verified symbolic hypotheses.

The execution engine itself never contains algorithm
implementations.

Execution is delegated to

• Prolog
• DeepProbLog
• Symbolic Executor

=========================================================
"""

import time


class ExecutionEngine:

    def __init__(self,
                 symbolic_executor,
                 prolog_executor=None,
                 neural_model=None):

        self.symbolic_executor = symbolic_executor
        self.prolog_executor = prolog_executor
        self.neural_model = neural_model

    # =====================================================

    def execute(self,
                hypothesis,
                input_data):

        start = time.time()

        result = self.symbolic_executor.execute(

            hypothesis,

            input_data

        )

        end = time.time()

        return {

            "description": hypothesis.get(
                "description",
                ""
            ),

            "input": input_data,

            "output": result,

            "execution_time": end - start,

            "status": "SUCCESS"

        }

    # =====================================================

    def batch_execute(self,
                      hypotheses,
                      inputs):

        outputs = []

        for hypothesis, data in zip(hypotheses, inputs):

            outputs.append(

                self.execute(

                    hypothesis,

                    data

                )

            )

        return outputs