"""
=========================================================
Universal Prompt Builder
=========================================================

Builds a compact but highly constrained prompt for
symbolic program induction.

Only training examples are exposed to the LLM.

Internal symbolic knowledge is intentionally hidden
to avoid biasing hypothesis generation.

=========================================================
"""


class PromptBuilder:

    def __init__(self):
        pass

    # =====================================================

    def _format_examples(self, knowledge):

        lines = []

        for obj in knowledge:

            ex = obj.example

            lines.append("=" * 60)
            lines.append(f"Training Example {ex.example_id}")
            lines.append("=" * 60)

            lines.append("Input:")
            lines.append(str(ex.input_data))
            lines.append("")

            lines.append("Expected Output:")
            lines.append(str(ex.output_data))
            lines.append("")

        return "\n".join(lines)

    # =====================================================

    def build(
    self,
    knowledge,
    contexts=None,
    user_context=None
    ):
        examples = self._format_examples(knowledge)

        prompt = f"""
You are an expert in

- Neuro-Symbolic AI
- Inductive Logic Programming (ILP)
- Program Synthesis
- DeepProbLog
- SWI-Prolog

Your task is to infer the hidden symbolic transformation
performed by an UNKNOWN black-box.

Learn ONLY from the training examples.

Never assume any known algorithm unless EVERY example
uniquely proves it.

==================================================
TRAINING EXAMPLES
==================================================

{examples}

==================================================
OBJECTIVE
==================================================

Infer the symbolic transformation and generate
EXACTLY THREE executable SWI-Prolog hypotheses.

Each hypothesis must represent a DIFFERENT symbolic
explanation while correctly explaining ALL examples.

==================================================
SYMBOLIC CONSTRAINTS
==================================================

1. Learn ONLY from the examples.

2. Never invent unsupported operations.

3. Never invent constants or elements.

4. Preserve data unless every example proves a change.

5. Reject any hypothesis that fails even ONE example.

6. Every hypothesis must be executable.

7. Every hypothesis must contain exactly ONE
   transform(Input, Output) rule.

8. Every predicate called by transform/2 must be
   completely defined.

9. Helper predicates must be reachable, executable,
   and contribute to the final output.

10. Recursive predicates must contain a terminating
    base case and a correct recursive clause.

11. No undefined predicates.

12. No placeholder predicates.

13. No dead code.

14. Generate valid SWI-Prolog only.

15. Confidence must reflect correctness across ALL
    training examples.

16. Hypotheses must be ranked from highest confidence
    to lowest confidence.

17. Before returning the result mentally verify

    ✓ transform/2 exists

    ✓ all predicates are defined

    ✓ recursion terminates

    ✓ rules execute correctly

    ✓ output matches every training example

18. Return ONLY valid JSON.

==================================================
OUTPUT FORMAT
==================================================

{{
    "problem_type": "",

    "reasoning": "",

    "hypotheses":
    [
        {{
            "id": 1,

            "description": "",

            "predicates": [],

            "rules":
            [
                "transform(Input, Output) :- helper(Input, Output)."
            ],

            "confidence": 0.95
        }},

        {{
            "id": 2,

            "description": "",

            "predicates": [],

            "rules": [],

            "confidence": 0.85
        }},

        {{
            "id": 3,

            "description": "",

            "predicates": [],

            "rules": [],

            "confidence": 0.75
        }}
    ]
}}

The response must satisfy ALL of the following

• Output ONLY the JSON object.

• The FIRST character must be '{{'.

• The LAST character must be '}}'.

• Do NOT output Markdown.

• Do NOT explain outside the JSON.

• Do NOT wrap the JSON inside ```.

"""

        return prompt.strip()