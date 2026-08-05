"""
============================================================
Context Engine
============================================================

Combines

1. Semantic Context
2. Behaviour Context
3. Pattern Context
4. Optional User Domain Context

into a unified context for every training example.

The additional user context is OPTIONAL.
If the user presses ENTER, the pipeline behaves exactly
as before.

============================================================
"""

from context.semantic_context import SemanticContext
from context.behavior_context import BehaviorContext
from context.pattern_context import PatternContext


class ContextEngine:

    def __init__(self):

        self.semantic = SemanticContext()
        self.behavior = BehaviorContext()
        self.pattern = PatternContext()

        # Optional domain knowledge supplied by user
        self.user_context = ""

    # =====================================================

    def set_user_context(self, context):

        if context is None:
            self.user_context = ""
            return

        self.user_context = str(context).strip()

    # =====================================================

    def ask_user_context(self):

        print("\n" + "=" * 60)
        print("OPTIONAL DOMAIN CONTEXT")
        print("=" * 60)

        print("If you have any additional domain knowledge")
        print("that may help explain the hidden transformation,")
        print("you may enter it below.")
        print()

        print("Examples")
        print("--------")
        print("Computational Fluid Dynamics")
        print("Aeroplane Wing Simulation")
        print("Medical Diagnosis")
        print("Financial Risk Analysis")
        print("Robot Navigation")
        print()

        print("Press ENTER to skip.")

        context = input("\nAdditional Context : ").strip()

        self.user_context = context

        return context

    # =====================================================

    def generate(self, knowledge):

        # Ask only once
        if self.user_context == "":
            self.ask_user_context()

        semantic_info = self.semantic.extract(knowledge)
        behavior_info = self.behavior.extract(knowledge)
        pattern_info = self.pattern.extract(knowledge)

        contexts = []

        for item in knowledge:

            contexts.append({

                "example": item.example,

                "context": self.build_context(

                    item,
                    semantic_info,
                    behavior_info,
                    pattern_info

                ),

                "semantics": semantic_info,

                "behaviors": behavior_info,

                "patterns": pattern_info,

                "user_context": self.user_context

            })

        return contexts

    # =====================================================

    def build_context(

        self,
        knowledge,
        semantics,
        behaviors,
        patterns

    ):

        lines = []

        lines.append("=" * 60)
        lines.append("SEMANTIC CONTEXT")
        lines.append("=" * 60)

        for s in semantics:
            lines.append(str(s))

        lines.append("")

        lines.append("=" * 60)
        lines.append("BEHAVIOUR CONTEXT")
        lines.append("=" * 60)

        for b in behaviors:
            lines.append(str(b))

        lines.append("")

        lines.append("=" * 60)
        lines.append("PATTERN CONTEXT")
        lines.append("=" * 60)

        for p in patterns:
            lines.append(str(p))

        lines.append("")

        # =====================================================
        # OPTIONAL USER CONTEXT
        # =====================================================

        if self.user_context:

            lines.append("=" * 60)
            lines.append("USER DOMAIN CONTEXT")
            lines.append("=" * 60)

            lines.append(self.user_context)

            lines.append("")

        # =====================================================

        lines.append("=" * 60)
        lines.append("FACTS")
        lines.append("=" * 60)

        for fact in knowledge.facts:
            lines.append(str(fact))

        lines.append("")

        lines.append("=" * 60)
        lines.append("PROPERTIES")
        lines.append("=" * 60)

        for key, value in knowledge.properties.items():
            lines.append(f"{key} : {value}")

        lines.append("")

        lines.append("=" * 60)
        lines.append("RELATIONS")
        lines.append("=" * 60)

        for relation in knowledge.relations:
            lines.append(str(relation))

        lines.append("")

        lines.append("=" * 60)
        lines.append("FEATURES")
        lines.append("=" * 60)

        for key, value in knowledge.features.items():
            lines.append(f"{key} : {value}")

        return "\n".join(lines)