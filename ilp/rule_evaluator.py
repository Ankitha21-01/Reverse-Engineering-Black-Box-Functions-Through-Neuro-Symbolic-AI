"""
=========================================================
Universal Rule Evaluator
=========================================================

Evaluates symbolic hypotheses using actual Prolog execution.

Metrics

✓ Support
✓ Coverage
✓ Partial Accuracy
✓ Execution Success Rate
✓ Predicate Count
✓ Rule Count
✓ Executability
✓ Evaluation Score

=========================================================
"""

import os
import tempfile

from prolog.prolog_executor import PrologExecutor


class RuleEvaluator:

    def __init__(self):

        self.executor = PrologExecutor()

    # =====================================================

    def _write_program(self, rules):

        fd, filename = tempfile.mkstemp(
            suffix=".pl",
            text=True
        )

        with os.fdopen(fd, "w") as f:

            for rule in rules:

                rule = str(rule).strip()

                if not rule.endswith("."):
                    rule += "."

                f.write(rule + "\n")

        return filename

    # =====================================================

    def _accuracy(self, expected, actual):
        """
        Computes partial accuracy between expected
        and actual outputs.
        """

        if expected == actual:
            return 1.0

        if actual is None:
            return 0.0

        if isinstance(expected, list) and isinstance(actual, list):

            if len(expected) == 0:
                return 1.0

            correct = 0

            for e, a in zip(expected, actual):
                if e == a:
                    correct += 1

            return correct / len(expected)

        return 0.0

    # =====================================================

    def evaluate(self, hypotheses, dataset):

        evaluated = []

        total_examples = max(len(dataset), 1)

        for hypothesis in hypotheses:

            support = 0
            execution_success = 0
            total_accuracy = 0.0

            predicate_count = len(
                hypothesis.get("predicates", [])
            )

            rule_count = len(
                hypothesis.get("rules", [])
            )

            program = self._write_program(
                hypothesis.get("rules", [])
            )

            try:

                for i, example in enumerate(dataset, start=1):

                    try:

                        input_data = example.input_data
                        expected_output = example.output_data

                    except AttributeError:

                        input_data = example["input"]
                        expected_output = example["output"]

                    if isinstance(input_data, dict) and len(input_data) == 1:
                        input_data = next(iter(input_data.values()))

                    if isinstance(expected_output, dict) and len(expected_output) == 1:
                        expected_output = next(iter(expected_output.values()))

                    result = self.executor.execute(
                        program,
                        input_data
                    )

                    actual_output = result.get("output")

                    if result["status"] == "SUCCESS":
                        execution_success += 1

                    accuracy = self._accuracy(
                        expected_output,
                        actual_output
                    )

                    total_accuracy += accuracy

                    print("\n" + "=" * 60)
                    print(f"Training Example {i}")
                    print("=" * 60)
                    print("Input            :", input_data)
                    print("Expected Output  :", expected_output)
                    print("Actual Output    :", actual_output)
                    print("Status           :", result["status"])
                    print("Query            :", result.get("query", ""))

                    if result["status"] != "SUCCESS":
                        print("Execution Error  :", result.get("error", ""))

                    print("Accuracy         :", round(accuracy, 3))

                    if accuracy == 1.0:
                        print("Result           : MATCH")
                        support += 1
                    else:
                        print("Result           : MISMATCH")

            finally:

                if os.path.exists(program):
                    os.remove(program)

            coverage = round(
                support / total_examples,
                3
            )

            average_accuracy = round(
                total_accuracy / total_examples,
                3
            )

            execution_success_rate = round(
                execution_success / total_examples,
                3
            )

            executable = (
                execution_success_rate >= 0.90
                and average_accuracy >= 0.80
            )

            evaluation_score = round(

                (
                    average_accuracy * 0.70
                    + coverage * 0.20
                    + hypothesis.get("confidence", 0.0) * 0.10
                ),

                3

            )

            hypothesis["verified"] = executable
            hypothesis["execution_ready"] = executable
            hypothesis["fully_executable"] = executable

            hypothesis["support"] = support
            hypothesis["coverage"] = coverage

            hypothesis["average_accuracy"] = average_accuracy
            hypothesis["execution_success_rate"] = execution_success_rate

            hypothesis["predicate_count"] = predicate_count
            hypothesis["rule_count"] = rule_count

            hypothesis["evaluation_score"] = evaluation_score
            hypothesis["executable"] = executable

            evaluated.append(hypothesis)

        return evaluated