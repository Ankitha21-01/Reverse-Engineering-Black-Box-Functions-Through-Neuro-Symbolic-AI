"""
============================================================
Human-in-the-Loop Neuro-Symbolic AI Framework
============================================================

Pipeline

Input CSV
    ↓
Unknown Black Box
    ↓
CSV Reader
    ↓
Dataset Parser
    ↓
Knowledge Generation
    ↓
Automatic Context Generation
    ↓
Optional Human Context
    ↓
Merged Context
    ↓
LLM Analysis
    ↓
ILP Learning
    ↓
DeepProbLog Verification
    ↓
Automatic Training Verification
    ↓
Prolog Generation
    ↓
Human Feedback
    ↓
Knowledge Persistence
    ↓
Iterative Learning
    ↓
Execution
============================================================
"""

import ast
import json
import os
from datetime import datetime

from config import *

from utils.logger import Logger

from blackbox.blackbox import UnknownBlackBox

from parser.csv_reader import CSVReader
from parser.parser import DatasetParser

from knowledge.knowledge_generator import KnowledgeGenerator

from context.context_engine import ContextEngine

from llm.llm_engine import LLMEngine
from llm.response_validator import ResponseValidator

from ilp.hypothesis_manager import HypothesisManager
from ilp.hypothesis_aggregator import HypothesisAggregator
from ilp.ilp_engine import ILPEngine
from ilp.predicate_refiner import PredicateRefiner
from ilp.rule_generalizer import RuleGeneralizer
from ilp.rule_evaluator import RuleEvaluator
from ilp.rule_ranker import RuleRanker
from ilp.executable_rule_generator import ExecutableRuleGenerator
from ilp.best_hypothesis_selector import BestHypothesisSelector

from deepproblog.verifier import DeepProbLogVerifier
from deepproblog.confidence_estimator import ConfidenceEstimator
from deepproblog.reasoning_engine import ReasoningEngine

from prolog.prolog_generator import PrologGenerator
from prolog.prolog_validator import PrologValidator
from prolog.rule_normalizer import RuleNormalizer
from prolog.prolog_executor import PrologExecutor

from executor.inference_engine import InferenceEngine

from evaluation.execution_metrics import ExecutionMetrics

logger = Logger()

# ==========================================================
# Knowledge Memory File
# ==========================================================

KNOWLEDGE_MEMORY = "accepted_hypotheses.json"

# ==========================================================
# Utility Functions
# ==========================================================

def header():

    print("=" * 80)
    print(" HUMAN-IN-THE-LOOP NEURO-SYMBOLIC AI FRAMEWORK ")
    print("=" * 80)


def section(title):

    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)


# ==========================================================
# Load Previous Knowledge
# ==========================================================

def load_previous_knowledge():

    if not os.path.exists(KNOWLEDGE_MEMORY):
        return []

    try:

        with open(KNOWLEDGE_MEMORY, "r") as file:

            return json.load(file)

    except Exception:

        return []


# ==========================================================
# Save Accepted Hypothesis
# ==========================================================

def save_hypothesis(
    hypothesis,
    problem_type,
    domain,
    user_context,
    training_examples
):

    memory = load_previous_knowledge()

    memory.append({

        "timestamp":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "problem_type":
            problem_type,

        "description":
            hypothesis.get("description", ""),

        "confidence":
            hypothesis.get("confidence", 0),

        "rules":
            hypothesis.get("rules", []),

        "domain":
            domain,

        "user_context":
            user_context,

        "training_examples":
            training_examples

    })

    with open(KNOWLEDGE_MEMORY, "w") as file:

        json.dump(

            memory,

            file,

            indent=4

        )


# ==========================================================
# Optional Human Context
# ==========================================================

def get_user_context():

    print()
    print("=" * 70)
    print("OPTIONAL DOMAIN CONTEXT")
    print("=" * 70)

    answer = input(

        "Would you like to provide additional domain knowledge? (y/n): "

    ).strip().lower()

    if answer != "y":

        return "", ""

    domain = input(

        "\nDomain Name : "

    ).strip()

    print()

    print(

        "Enter context (Press ENTER twice to finish)\n"

    )

    lines = []

    while True:

        line = input()

        if line == "":

            break

        lines.append(line)

    return domain, "\n".join(lines)


# ==========================================================
# Merge Human Context
# ==========================================================

def merge_user_context(

    contexts,

    domain,

    user_context

):

    if not domain:

        return contexts

    for context in contexts:

        context["context"] += (

            "\n\n"

            + "=" * 60

            + "\nUSER DOMAIN CONTEXT\n"

            + "=" * 60

            + f"\nDomain : {domain}\n\n"

            + user_context

        )

    return contexts


# ==========================================================
# Training Verification
# ==========================================================

def verify_training_examples(

    executor,

    hypothesis,

    dataset

):

    print()

    print("=" * 70)
    print("TRAINING EXAMPLE VERIFICATION")
    print("=" * 70)

    correct = 0

    total = len(dataset)

    for example in dataset:

        input_data = example.input_data
        expected_output = example.output_data

        if isinstance(input_data, dict) and len(input_data) == 1:
            input_data = next(iter(input_data.values()))

        if isinstance(expected_output, dict) and len(expected_output) == 1:
            expected_output = next(iter(expected_output.values()))

        result = executor.execute(
            hypothesis["prolog_file"],
            input_data
        )
        print("\nReturned dictionary:")
        print(result)
        passed = (
            result["status"] == "SUCCESS"
            and
            result["output"] == expected_output
        )

        if passed:

            correct += 1

            print(f"Example {example.example_id:<5} ✓")

        else:

            print(f"Example {example.example_id:<5} ✗")

            print("Expected :", expected_output)

            print("Produced :", result["output"])

    accuracy = correct / total if total else 0

    print()

    print(

        f"Training Accuracy : {accuracy:.2%}"

    )

    return accuracy
# ==========================================================
# Main
# ==========================================================

def main():

    header()

    # ======================================================
    # STEP 1 : UNKNOWN BLACK BOX
    # ======================================================

    section("STEP 1 : UNKNOWN BLACK BOX")

    blackbox = UnknownBlackBox(
        INPUT_CSV,
        OUTPUT_CSV
    )

    blackbox.observe()

    # ======================================================
    # STEP 2 : READING DATASET
    # ======================================================

    section("STEP 2 : READING DATASET")

    reader = CSVReader(
        INPUT_CSV,
        OUTPUT_CSV
    )

    input_df, output_df = reader.load()

    # ======================================================
    # STEP 3 : PARSING DATASET
    # ======================================================

    section("STEP 3 : PARSING DATASET")

    parser = DatasetParser()

    dataset = parser.parse(
        input_df,
        output_df
    )

    print()

    for example in dataset:
        print(example)

    # ======================================================
    # STEP 4 : KNOWLEDGE GENERATION
    # ======================================================

    section("STEP 4 : KNOWLEDGE GENERATION")

    knowledge_generator = KnowledgeGenerator()

    knowledge = knowledge_generator.generate(
        dataset
    )

    knowledge_generator.print_summary(
        knowledge
    )

    # ======================================================
    # Previous Learned Knowledge
    # ======================================================

    previous_memory = load_previous_knowledge()

    print()

    print(
        f"Previously Accepted Knowledge : {len(previous_memory)}"
    )

    # ======================================================
    # STEP 5 : CONTEXT GENERATION
    # ======================================================

    section("STEP 5 : CONTEXT GENERATION")

    context_engine = ContextEngine()

    contexts = context_engine.generate(
        knowledge
    )

    # ======================================================
    # OPTIONAL HUMAN CONTEXT
    # ======================================================

    domain, user_context = get_user_context()

    contexts = merge_user_context(
        contexts,
        domain,
        user_context
    )

    # ======================================================
    # Display Final Context
    # ======================================================

    for context in contexts:

        print()

        print(
            "Example :",
            context["example"].example_id
        )

        print(
            context["context"]
        )

    # ======================================================
    # STEP 6 : LLM ANALYSIS
    # ======================================================

    section("STEP 6 : LLM ANALYSIS")

    llm = LLMEngine()

    llm_result = llm.analyze(
        knowledge,
        contexts
    )

    validator = ResponseValidator()

    llm_result = validator.validate(
        llm_result
    )

    if not llm_result.get("success", False):

        print()

        print("LLM Analysis Failed")

        return

    print()

    print("=" * 70)
    print("DETECTED PROBLEM TYPE")
    print("=" * 70)

    print(
        llm_result["problem_type"]
    )

    print()

    print("=" * 70)
    print("LLM REASONING")
    print("=" * 70)

    print(
        llm_result["reasoning"]
    )

    print()

    print("=" * 70)
    print("GENERATED HYPOTHESES")
    print("=" * 70)

    for i, hypothesis in enumerate(

        llm_result["hypotheses"],

        start=1

    ):

        print()

        print(f"Hypothesis {i}")

        print("-" * 60)

        print(
            "Description :",
            hypothesis["description"]
        )

        print(
            "Confidence :",
            hypothesis["confidence"]
        )

        print()

        print("Predicates")

        for predicate in hypothesis.get(
            "predicates",
            []
        ):

            print(
                " ",
                predicate
            )

        print()

        print("Rules")

        for rule in hypothesis.get(
            "rules",
            []
        ):

            print(
                " ",
                rule
            )

        print("-" * 60)

    # ======================================================
    # STEP 7 : HYPOTHESIS MANAGEMENT
    # ======================================================

    section("STEP 7 : HYPOTHESIS MANAGEMENT")

    manager = HypothesisManager()

    ranked = manager.process(
        llm_result
    )

    aggregator = HypothesisAggregator()

    aggregated = aggregator.aggregate(
        ranked
    )

    print()

    print(
        "Total Aggregated Hypotheses :",
        len(aggregated)
    )

    # ======================================================
    # STEP 8 : ILP LEARNING
    # ======================================================

    section("STEP 8 : ILP LEARNING")

    ilp = ILPEngine()

    learned = ilp.learn(
        aggregated,
        knowledge
    )

    print()

    print(
        "Initial Learned Rules :",
        len(learned)
    )

        # ======================================================
    # Predicate Refinement
    # ======================================================

    section("STEP 9 : PREDICATE REFINEMENT")

    refiner = PredicateRefiner()

    refined = refiner.refine(
        learned
    )

    print()

    print("Refined Hypotheses :", len(refined))

    # ======================================================
    # Rule Generalization
    # ======================================================

    section("STEP 10 : RULE GENERALIZATION")

    generalizer = RuleGeneralizer()

    generalized = generalizer.generalize(
        refined
    )

    print()

    print("Generalized Rules :", len(generalized))

    # ======================================================
    # Rule Evaluation
    # ======================================================

    section("STEP 11 : RULE EVALUATION")

    evaluator = RuleEvaluator()

    evaluated = evaluator.evaluate(

        generalized,

        dataset

    )

    print()

    print("Evaluated Rules :", len(evaluated))

    # ======================================================
    # Rule Ranking
    # ======================================================

    section("STEP 12 : RULE RANKING")

    ranker = RuleRanker()

    ranked_rules = ranker.rank(
        evaluated
    )

    print()

    print("=" * 70)
    print("RANKED RULES")
    print("=" * 70)

    for index, rule in enumerate(

        ranked_rules,

        start=1

    ):

        print()

        print(f"Rule {index}")

        print("-" * 60)

        print(

            "Description :",

            rule.get(

                "description",

                ""

            )

        )

        print(

            "Support :",

            rule.get(

                "support",

                0

            )

        )

        print(

            "Coverage :",

            rule.get(

                "coverage",

                0

            )

        )

        print(

            "Learning Score :",

            rule.get(

                "learning_score",

                0

            )

        )

        print(

            "Ranking Score :",

            rule.get(

                "ranking_score",

                0

            )

        )

        print(

            "Executable :",

            rule.get(

                "executable",

                False

            )

        )

    # ======================================================
    # Executable Rule Generation
    # ======================================================

    section("STEP 13 : EXECUTABLE RULE GENERATION")

    executable_generator = ExecutableRuleGenerator()

    executable_rules = executable_generator.generate(

        ranked_rules

    )

    validator = PrologValidator()

    validated_rules = []

    for hypothesis in executable_rules:

        validated = validator.validate(

            hypothesis

        )

        validated_rules.append(

            validated

        )

    executable_rules = validated_rules

    print()

    print("=" * 70)
    print("EXECUTABLE PROGRAMS")
    print("=" * 70)

    for hypothesis in executable_rules:

        print()

        print(

            "Description :",

            hypothesis["description"]

        )

        print(

            "Executable Rules :",

            hypothesis["executable_rules"]

        )

        print(

            "Total Rules :",

            hypothesis["total_rules"]

        )

        print(

            "Fully Executable :",

            hypothesis["fully_executable"]

        )

        print(

            "Ranking Score :",

            hypothesis.get(

                "ranking_score",

                0

            )

        )

        print("-" * 60)

    # ======================================================
    # Select Best Hypothesis
    # ======================================================

    section("STEP 14 : BEST HYPOTHESIS SELECTION")

    selector = BestHypothesisSelector()

    best_hypothesis = selector.select(

        executable_rules

    )

    if best_hypothesis is None:

        print()

        print("No executable hypothesis found.")

        return

    print()

    print("=" * 70)
    print("BEST HYPOTHESIS")
    print("=" * 70)

    print(

        "Description :",

        best_hypothesis["description"]

    )

    print(

        "Confidence :",

        best_hypothesis["confidence"]

    )

    print(

        "Ranking Score :",

        best_hypothesis.get(

            "ranking_score",

            0

        )

    )

    print(

        "Learning Score :",

        best_hypothesis.get(

            "learning_score",

            0

        )

    )

    print()

    # ======================================================
    # Prolog Generation
    # ======================================================

    section("STEP 15 : PROLOG GENERATION")

    normalizer = RuleNormalizer()

    best_hypothesis = normalizer.normalize(

        [best_hypothesis]

    )[0]

    generator = PrologGenerator(

        output_file="generated/best_rules.pl"

    )

    print("\n==============================")
    print("RULES BEFORE PROLOG GENERATION")
    print("==============================")

    print("Rules:")
    for r in best_hypothesis.get("rules", []):
        print("  ", r)

    print("\nExecutable Rules:")
    for r in best_hypothesis.get("executable_rules", []):
        print("  ", r)

    print("==============================\n")

    generated_file = generator.generate(

        best_hypothesis

    )

    best_hypothesis["prolog_file"] = generated_file

    print()

    print("Generated File")

    print(generated_file)

        # ======================================================
    # STEP 16 : DEEPPROBLOG VERIFICATION
    # ======================================================

    section("STEP 16 : DEEPPROBLOG VERIFICATION")

    verifier = DeepProbLogVerifier()

    verified = verifier.verify(
        [best_hypothesis]
    )

    best_hypothesis = verified[0]

    estimator = ConfidenceEstimator()

    confidence = estimator.estimate(
        [best_hypothesis]
    )[0]

    reasoning_engine = ReasoningEngine()

    explanation = reasoning_engine.explain(
        [best_hypothesis]
    )[0]

    print()

    print("=" * 70)
    print("SELECTED HYPOTHESIS")
    print("=" * 70)

    print(
        "Description :",
        best_hypothesis["description"]
    )

    print(
        "Verified :",
        best_hypothesis["verified"]
    )

    print(
        "Confidence :",
        confidence["score"]
    )

    print()

    print(
        explanation["explanation"]
    )

    if not best_hypothesis["verified"]:

        print()

        print(
            "DeepProbLog verification failed."
        )

        return

    # ======================================================
    # STEP 17 : TRAINING EXAMPLE VERIFICATION
    # ======================================================

    section("STEP 17 : TRAINING EXAMPLE VERIFICATION")

    executor = PrologExecutor()

    training_accuracy = verify_training_examples(

        executor,

        best_hypothesis,

        dataset

    )

    best_hypothesis["training_accuracy"] = training_accuracy

    if training_accuracy < 1.0:

        print()

        print("=" * 70)
        print("WARNING")
        print("=" * 70)

        print(

            "Generated symbolic program does NOT "

            "correctly reproduce all training examples."

        )

        print()

        print(

            f"Training Accuracy : "

            f"{training_accuracy:.2%}"

        )

        print()

        answer = input(

            "Continue anyway? (yes/no): "

        ).strip().lower()

        if answer != "yes":

            print()

            print("Execution stopped.")

            return

    else:

        print()

        print("=" * 70)

        print("SUCCESS")

        print("=" * 70)

        print(

            "All training examples reproduced correctly."

        )

        print()

        print(

            f"Training Accuracy : "

            f"{training_accuracy:.2%}"

        )

    # ======================================================
    # STEP 13 : SYMBOLIC EXECUTION
    # ======================================================

    section("STEP 18 : SYMBOLIC EXECUTION")

    print()
    print("Enter unseen input")
    print("-" * 60)
    print("[5,4,3,2,1]")
    print("{'capacity':10,'weights':[2,3],'values':[5,8]}")
    print("{'graph':{'A':['B']}}")
    print("[[1,2],[3,4]]")
    print("'hello world'")
    print()

    raw = input("Input : ")

    try:
        new_input = ast.literal_eval(raw)
    except Exception:
        new_input = raw

    print()
    print("=" * 70)
    print("EXECUTING SELECTED HYPOTHESIS")
    print("=" * 70)

    print("Description :", best_hypothesis["description"])
    print("Confidence  :", best_hypothesis.get("confidence", 0))
    print("Verified    :", best_hypothesis.get("verified", False))
    print()

    executor = PrologExecutor()

    result = executor.execute(

        best_hypothesis["prolog_file"],

        new_input

    )

    print("=" * 70)
    print("EXECUTION RESULT")
    print("=" * 70)

    print("Status           :", result["status"])
    print("Query            :", result.get("query", ""))
    print("Input            :", result.get("input"))
    print("Output           :", result.get("output"))
    print("Bindings         :", result.get("bindings", {}))
    print("Execution Time   :", result["execution_time"], "seconds")

    if result.get("error"):

        print("Error            :", result["error"])

    # ------------------------------------------------------
    # Store execution metadata
    # ------------------------------------------------------

    best_hypothesis["last_execution"] = {

        "status": result["status"],

        "input": result.get("input"),

        "output": result.get("output"),

        "execution_time": result["execution_time"]

    }

    # ------------------------------------------------------
    # Quick execution summary
    # ------------------------------------------------------

    print()

    if result["status"] == "SUCCESS":

        print("Execution completed successfully.")

    elif result["status"] == "NO_SOLUTION":

        print("Program executed but produced no solution.")

    else:

        print("Execution failed.")

    # ======================================================
    # STEP 14 : INFERENCE
    # ======================================================

    section("STEP 19 : INFERENCE")

    inference_engine = InferenceEngine()

    inference = inference_engine.infer(result)

    print()

    print("=" * 70)
    print("INFERENCE RESULT")
    print("=" * 70)

    inference_engine.explain(inference)

    # ------------------------------------------------------
    # Store inference for later stages
    # ------------------------------------------------------

    best_hypothesis["last_inference"] = inference

    # ------------------------------------------------------
    # Simple symbolic interpretation
    # ------------------------------------------------------

    print()

    if result["status"] == "SUCCESS":

        print("Inference Status : SUCCESS")

        print(
            "The learned symbolic program successfully produced an output "
            "for the unseen input."
        )

    elif result["status"] == "NO_SOLUTION":

        print("Inference Status : NO SOLUTION")

        print(
            "The symbolic program executed correctly, but no valid "
            "solution could be derived for this input."
        )

    else:

        print("Inference Status : FAILED")

        print(
            "The symbolic program could not complete execution."
        )

    print()

    print("Inference completed.")

    # ======================================================
    # STEP 15 : EXECUTION METRICS
    # ======================================================

    section("STEP 20 : EXECUTION METRICS")

    metrics = ExecutionMetrics()

    report = metrics.evaluate(result)

    print()

    print("=" * 70)
    print("EXECUTION METRICS")
    print("=" * 70)

    for key, value in report.items():

        print(f"{key:25}: {value}")

    # ------------------------------------------------------
    # Store execution metrics
    # ------------------------------------------------------

    best_hypothesis["execution_report"] = report

    # ------------------------------------------------------
    # Overall summary
    # ------------------------------------------------------

    print()

    success = report.get("success", False)

    if success:

        print("Overall Status : SUCCESS")

    else:

        print("Overall Status : FAILED")

    print()

    print("Execution Summary")

    print("-" * 60)

    print("Problem Type       :", llm_result["problem_type"])

    print("Hypothesis         :", best_hypothesis["description"])

    print("Verified           :", best_hypothesis.get("verified", False))

    print("Execution Status   :", result["status"])

    print("Execution Time     :", result["execution_time"])

    print("Overall Success    :", success)

    if result.get("output") is not None:

        print("Generated Output   :", result["output"])

    else:

        print("Generated Output   : None")

    print()

    print("Execution metrics recorded successfully.")

    # ======================================================
    # STEP 16 : HUMAN KNOWLEDGE UPDATE
    # ======================================================

    section("STEP 21 : HUMAN KNOWLEDGE UPDATE")

    print()
    print("Would you like to provide additional domain knowledge?")
    print()
    print("Examples:")
    print("  • In Computational Fluid Dynamics, turbulence increases drag.")
    print("  • Aircraft wings generate lift because of pressure difference.")
    print("  • A graph may contain weighted edges.")
    print("  • Sorted arrays preserve ascending order.")
    print()

    choice = input(
        "Add additional knowledge? (yes/no): "
    ).strip().lower()

    additional_context = []

    if choice == "yes":

        print()

        print("Enter one statement at a time.")

        print("Press ENTER on an empty line to finish.")

        while True:

            statement = input("Knowledge : ").strip()

            if statement == "":

                break

            additional_context.append(statement)

        if additional_context:

            best_hypothesis["human_context"] = additional_context

            print()

            print("=" * 70)
            print("NEW DOMAIN KNOWLEDGE")
            print("=" * 70)

            for i, statement in enumerate(
                additional_context,
                start=1
            ):

                print(f"{i}. {statement}")

        else:

            print()

            print("No additional knowledge was entered.")

    else:

        print()

        print("No additional domain knowledge added.")

        best_hypothesis["human_context"] = []

    print()

    print("Total Human Knowledge Entries :",

          len(best_hypothesis["human_context"]))

        # ======================================================
    # STEP 17 : FINAL SUMMARY
    # ======================================================

    section("STEP 22 : FINAL FRAMEWORK SUMMARY")

    print()

    print("=" * 80)
    print("FRAMEWORK EXECUTION SUMMARY")
    print("=" * 80)

    print()

    print("Problem Type          :", llm_result["problem_type"])

    print("Selected Hypothesis   :")

    print("   ", best_hypothesis["description"])

    print()

    print("Verification Status   :",

          "PASSED" if best_hypothesis.get("verified", False)

          else "FAILED")

    print()

    print("Execution Status      :", result["status"])

    print("Execution Time (sec)  :",

          result["execution_time"])

    print()

    print("Generated Output")

    print("-" * 60)

    print(result.get("output"))

    print()

    print("Human Knowledge Entries :",

          len(best_hypothesis.get("human_context", [])))

    if best_hypothesis.get("human_context"):

        print()

        print("Additional Domain Knowledge")

        print("-" * 60)

        for i, statement in enumerate(

                best_hypothesis["human_context"],

                start=1):

            print(f"{i}. {statement}")

    print()

    print("Execution Metrics")

    print("-" * 60)

    for key, value in report.items():

        print(f"{key:25}: {value}")

    print()

    print("=" * 80)

    if report.get("success", False):

        print("FRAMEWORK EXECUTED SUCCESSFULLY")

    else:

        print("FRAMEWORK EXECUTED WITH ERRORS")

    print("=" * 80)

    print()

    logger.info("Framework execution completed.")

# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":

    main()