"""
=========================================================
Universal LLM Engine
=========================================================

Responsible for

• Prompt Generation
• Groq Communication
• JSON Repair
• JSON Validation
• Hypothesis Validation
• Duplicate Removal
• Confidence Normalization
• Executability Checking
• Symbolic Ranking

Compatible with all modified modules.

=========================================================
"""

import json
import re

from llm.groq_client import GroqClient
from llm.prompt_builder import PromptBuilder
from llm.response_validator import ResponseValidator
from llm.json_repair import JSONRepair


class LLMEngine:

    def __init__(self):

        self.client = GroqClient()

        self.prompt_builder = PromptBuilder()

        self.validator = ResponseValidator()

        self.repair = JSONRepair()

        # ---------------------------------------------
        # Built-in SWI-Prolog predicates
        # ---------------------------------------------

        self.builtins = {

            "append",
            "member",
            "length",
            "reverse",
            "sort",
            "msort",
            "findall",
            "bagof",
            "setof",
            "nth0",
            "nth1",
            "integer",
            "number",
            "atom",
            "var",
            "nonvar",
            "is",
            "true",
            "fail"

        }

    # =====================================================

    def analyze(
        self,
        knowledge,
        contexts,
        user_context=None
    ):

        prompt = self.prompt_builder.build(

            knowledge,

            contexts,

            user_context=user_context

        )

        print("\nSending prompt to Groq...\n")

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            print(f"\nAttempt {attempt + 1}/{MAX_RETRIES}")

            response = self.client.generate(prompt)

            response = self.repair.clean(response)

            print("=" * 70)
            print("RAW LLM RESPONSE")
            print("=" * 70)
            print(response)

            try:

                parsed = json.loads(response)

            except Exception:

                try:

                    repaired = self.repair.repair(response)

                    parsed = json.loads(repaired)

                except Exception as e:

                    print("\nJSON Parsing Failed")

                    print(e)

                    continue

            parsed["raw_response"] = response

            parsed = self.validator.validate(parsed)

            valid_hypotheses = []

            seen_programs = set()

            rejection_reason = ""

            for hypothesis in parsed.get("hypotheses", []):

                # -------------------------------------
                # Validate structure
                # -------------------------------------

                if not isinstance(
                    hypothesis.get("rules"),
                    list
                ):

                    rejection_reason = "Rules not list"

                    continue

                if not isinstance(
                    hypothesis.get("predicates"),
                    list
                ):

                    rejection_reason = "Predicates not list"

                    continue

                if not hypothesis.get("description"):

                    rejection_reason = "Missing description"

                    continue

                rules = hypothesis.get("rules", [])

                predicates = hypothesis.get(
                    "predicates",
                    []
                )

                # -------------------------------------
                # Normalize confidence
                # -------------------------------------

                confidence = hypothesis.get(
                    "confidence",
                    0
                )

                try:

                    confidence = float(confidence)

                except Exception:

                    confidence = 0.0

                if confidence > 1:

                    confidence /= 100

                confidence = max(

                    0.0,

                    min(

                        confidence,

                        1.0

                    )

                )

                hypothesis["confidence"] = confidence

                # -------------------------------------
                # Must contain transform/2
                # -------------------------------------

                if not self._has_transform(rules):

                    rejection_reason = "Missing transform/2"

                    print(

                        "\nRejected:",

                        hypothesis.get(

                            "description",

                            ""

                        )

                    )

                    continue

                # -------------------------------------
                # Program completeness
                # -------------------------------------

                if not self._complete_program(rules):

                    rejection_reason = "Undefined helper predicate"

                    print(

                        "\nRejected:",

                        hypothesis.get(

                            "description",

                            ""

                        )

                    )

                    continue

                                # -------------------------------------
                # Duplicate program detection
                # -------------------------------------

                signature = tuple(

                    sorted(

                        rule.strip()

                        for rule in rules

                    )

                )

                if signature in seen_programs:

                    rejection_reason = "Duplicate hypothesis"

                    continue

                seen_programs.add(signature)

                # -------------------------------------
                # Metadata
                # -------------------------------------

                hypothesis["rule_count"] = len(rules)

                hypothesis["predicate_count"] = len(predicates)

                # -------------------------------------
                # Better symbolic score
                # -------------------------------------

                score = (

                    confidence * 100

                    +

                    5 * len(rules)

                    +

                    3 * len(predicates)

                )

                hypothesis["score"] = round(score, 3)

                valid_hypotheses.append(hypothesis)

            # -----------------------------------------
            # Success
            # -----------------------------------------

            if len(valid_hypotheses) >= 3:

                valid_hypotheses.sort(

                    key=lambda h: h["score"],

                    reverse=True

                )

                parsed["hypotheses"] = valid_hypotheses[:3]

                return {

                    "success": True,

                    "problem_type": parsed.get(

                        "problem_type",

                        "Unknown"

                    ),

                    "reasoning": parsed.get(

                        "reasoning",

                        ""

                    ),

                    "hypotheses": parsed["hypotheses"],

                    "raw_response": response

                }

            print(

                f"\nOnly {len(valid_hypotheses)} valid hypotheses generated."

            )

            if rejection_reason:

                print(

                    "Reason:",

                    rejection_reason

                )

            print("Retrying...\n")

        # -----------------------------------------
        # Failed after retries
        # -----------------------------------------

        return {

            "success": False,

            "problem_type": "Unknown",

            "reasoning": "",

            "hypotheses": [],

            "raw_response": "",

            "error": "Unable to generate three executable hypotheses."

        }

    # =====================================================

    def _has_transform(self, rules):

        for rule in rules:

            rule = rule.strip()

            if rule.startswith("transform("):

                return True

        return False

    # =====================================================

    def _complete_program(self, rules):

        """
        Checks that every helper predicate called
        is actually defined.
        """

        defined = set()

        called = set()

        for rule in rules:

            rule = rule.strip()

            if not rule:

                continue

            # -------------------------------------
            # Predicate definition
            # -------------------------------------

            head = rule.split(":-")[0]

            m = re.match(

                r'([a-z][A-Za-z0-9_]*)\s*\(',

                head

            )

            if m:

                defined.add(

                    m.group(1)

                )

            # -------------------------------------
            # Predicate calls
            # -------------------------------------

            if ":-" not in rule:

                continue

            body = rule.split(":-", 1)[1]

            calls = re.findall(

                r'([a-z][A-Za-z0-9_]*)\s*\(',

                body

            )

            for call in calls:

                if call in self.builtins:

                    continue

                called.add(call)

        # -----------------------------------------
        # Every helper predicate must exist
        # -----------------------------------------

        missing = [

            p

            for p in called

            if p not in defined

        ]

        if missing:

            print(

                "\nUndefined predicates:",

                ", ".join(missing)

            )

            return False

        return True