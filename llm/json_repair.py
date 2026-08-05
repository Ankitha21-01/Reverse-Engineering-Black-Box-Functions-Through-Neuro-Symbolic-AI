"""
============================================================
Universal JSON Repair Utility
============================================================

Repairs malformed JSON returned by the LLM.

Capabilities

✓ Removes markdown
✓ Removes introductory explanations
✓ Extracts the best JSON object
✓ Repairs smart quotes
✓ Removes trailing commas
✓ Repairs invalid backslashes
✓ Compresses excessive backslashes
✓ Balances braces
✓ Validates JSON structure
✓ Returns {} on failure

============================================================
"""

import re
import json


class JSONRepair:

    def __init__(self):
        pass

    # =====================================================

    def clean(self, text):
        return self.repair(text)

    # =====================================================

    def repair(self, text):

        if text is None:
            return "{}"

        text = str(text).strip()

        if not text:
            return "{}"

        # ---------------------------------------------
        # Cleaning pipeline
        # ---------------------------------------------

        text = self.remove_markdown(text)

        text = self.remove_explanations(text)

        text = self.replace_quotes(text)

        text = self.extract_json(text)

        text = self.remove_trailing_commas(text)

        text = self.fix_backslashes(text)

        text = self.compress_backslashes(text)

        text = self.balance_braces(text)

        # ---------------------------------------------
        # Final validation
        # ---------------------------------------------

        try:

            obj = json.loads(text)

            if not isinstance(obj, dict):
                return "{}"

            if "hypotheses" not in obj:
                return "{}"

            if not isinstance(obj["hypotheses"], list):
                return "{}"

            return json.dumps(obj, ensure_ascii=False)

        except Exception:

            return "{}"

    # =====================================================

    def remove_markdown(self, text):

        text = re.sub(
            r"```json",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```",
            "",
            text
        )

        return text.strip()

    # =====================================================

    def remove_explanations(self, text):

        phrases = [

            "Here is the JSON",
            "Here is your JSON",
            "Here is the corrected JSON",
            "The answer is",
            "Response:",
            "Output:",
            "JSON:",
            "Below is the JSON"

        ]

        for phrase in phrases:

            text = text.replace(
                phrase,
                ""
            )

        return text.strip()

    # =====================================================

    def extract_json(self, text):

        """
        Extracts the BEST JSON object.

        If multiple JSON objects exist,
        keep the one containing the largest
        hypothesis list.
        """

        candidates = []

        brace_positions = [

            m.start()

            for m in re.finditer(r"\{", text)

        ]

        for start in brace_positions:

            depth = 0

            for i in range(start, len(text)):

                ch = text[i]

                if ch == "{":
                    depth += 1

                elif ch == "}":

                    depth -= 1

                    if depth == 0:

                        candidate = text[start:i + 1].strip()

                        if '"hypotheses"' not in candidate:
                            break

                        try:

                            obj = json.loads(candidate)

                            if isinstance(obj, dict):

                                candidates.append(obj)

                        except Exception:
                            pass

                        break

        if not candidates:
            return "{}"

        best = max(

            candidates,

            key=lambda x: len(

                x.get(

                    "hypotheses",

                    []

                )

            )

        )

        return json.dumps(best, ensure_ascii=False)

    # =====================================================

    def replace_quotes(self, text):

        return (

            text

            .replace("“", '"')

            .replace("”", '"')

            .replace("‘", "'")

            .replace("’", "'")

        )

    # =====================================================

    def remove_trailing_commas(self, text):

        return re.sub(

            r",(\s*[}\]])",

            r"\1",

            text

        )

    # =====================================================

    def fix_backslashes(self, text):

        return re.sub(

            r'\\(?!["\\/bfnrtu])',

            r'\\\\',

            text

        )

    # =====================================================

    def compress_backslashes(self, text):

        return re.sub(

            r'\\\\+',

            r'\\\\',

            text

        )

    # =====================================================

    def balance_braces(self, text):

        opens = text.count("{")
        closes = text.count("}")

        if opens > closes:

            text += "}" * (opens - closes)

        elif closes > opens:

            diff = closes - opens

            while diff > 0 and text.startswith("}"):

                text = text[1:]

                diff -= 1

        return text.strip()