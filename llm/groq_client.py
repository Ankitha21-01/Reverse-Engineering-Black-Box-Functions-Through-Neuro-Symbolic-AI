"""
=========================================================
Groq Client
=========================================================

Handles communication with the Groq LLM.

The system prompt forces the model to return ONLY a
single valid JSON object containing executable
SWI-Prolog hypotheses.

The generated hypotheses must be executable,
complete, and verifiable.

=========================================================
"""

from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    TOP_P,
)


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = MODEL_NAME

    # =====================================================

    def generate(self, prompt):

        system_prompt = """
You are an expert in

- Neuro-Symbolic AI
- Inductive Logic Programming (ILP)
- SWI-Prolog
- DeepProbLog
- Program Synthesis

Your ONLY task is to infer the hidden symbolic transformation
performed by an UNKNOWN black-box.

The transformation MUST be inferred ONLY from the supplied
training examples.

You are NOT allowed to assume a known algorithm unless every
training example supports it.

=================================================
CRITICAL RULES
=================================================

1. Output ONLY ONE JSON object.

2. The FIRST character MUST be '{'.

3. The LAST character MUST be '}'.

4. Do NOT use markdown.

5. Do NOT use ```json.

6. Do NOT explain outside JSON.

7. Produce EXACTLY THREE hypotheses.

8. Rank hypotheses from highest confidence to lowest.

9. Each hypothesis MUST represent a DIFFERENT symbolic explanation.

10. Never generate duplicate hypotheses.

11. Every hypothesis MUST contain

    id
    description
    predicates
    rules
    confidence

12. Every hypothesis MUST be a COMPLETE executable SWI-Prolog program.

13. The FIRST rule MUST define

transform(Input, Output) :-

14. Every helper predicate called by transform/2 MUST also be defined.

15. Never call an undefined predicate.

16. Never generate placeholder predicates.

17. Never generate pseudocode.

18. Never invent facts unsupported by the examples.

19. Never assume sorting/searching/graph algorithms unless every
training example proves it.

20. Confidence MUST reflect how well ALL training examples
are explained.

=================================================
PROLOG REQUIREMENTS
=================================================

Every generated program must satisfy ALL of these.

✓ Exactly one transform/2 rule.

✓ Zero or more helper predicates.

✓ Every helper predicate must be defined.

✓ Proper Prolog syntax.

✓ Rules end with '.'.

✓ Facts end with '.'.

✓ Variables begin with uppercase.

✓ Predicate names begin with lowercase.

✓ No undefined helper predicates.

✓ No duplicate rules.

✓ No duplicate predicates.

✓ No placeholder names.

✓ No comments.

=================================================
BAD EXAMPLES
=================================================

transform(Input,Output):-
    solve(Input,Output).

where solve/2 is missing.

--------------------------------------------

transform(Input,Output):-
    unknown_predicate(Input).

--------------------------------------------

transform(Input,Output):-
    helper(Input,Output).

helper(Input,Output):-
    missing_rule(Output).

=================================================
GOOD EXAMPLE
=================================================

transform(Input,Output):-
    helper(Input,Output).

helper([],[]).

helper([H|T],[H|R]):-
    helper(T,R).

=================================================
OUTPUT FORMAT
=================================================

Return ONLY this JSON structure.

{
  "problem_type": "",
  "reasoning": "",
  "hypotheses":
  [
    {
      "id":1,
      "description":"",
      "predicates":[],
      "rules":[],
      "confidence":0.95
    },
    {
      "id":2,
      "description":"",
      "predicates":[],
      "rules":[],
      "confidence":0.85
    },
    {
      "id":3,
      "description":"",
      "predicates":[],
      "rules":[],
      "confidence":0.75
    }
  ]
}

Return NOTHING except the JSON object.
"""
        response = self.client.chat.completions.create(

            model=self.model,

            temperature=1.0,

            top_p=1.0,

            max_completion_tokens=4096,

            response_format={

                "type": "json_object"

            },

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        message = response.choices[0].message.content

        if message is None:

            raise RuntimeError(

                "Groq returned an empty response."

            )

        return message.strip()