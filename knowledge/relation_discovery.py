"""
============================================================
Universal Relation Discovery Engine (Version 2)
============================================================

Discovers symbolic relationships between input and output.

Features

✓ Domain independent
✓ Algorithm independent
✓ Structural relations
✓ Sequence relations
✓ Dictionary relations
✓ Numeric relations
✓ Supports future Context Engine

============================================================
"""

from collections import Counter
from copy import deepcopy


class RelationDiscovery:

    def __init__(self):
        pass

    # =====================================================

    def discover(self, example):

        relations = []

        inp = deepcopy(example.input_data)
        out = deepcopy(example.output_data)

        # -------------------------------------------------
        # Basic datatype relations
        # -------------------------------------------------

        relations.append({

            "relation": "input_type",

            "value": type(inp).__name__

        })

        relations.append({

            "relation": "output_type",

            "value": type(out).__name__

        })

        relations.append({

            "relation": "same_datatype",

            "value": type(inp) == type(out)

        })

        relations.append({

            "relation": "same_structure",

            "value": self.same_structure(inp, out)

        })

        relations.append({

            "relation": "same_value",

            "value": inp == out

        })

        relations.append({

            "relation": "input_size",

            "value": self.safe_length(inp)

        })

        relations.append({

            "relation": "output_size",

            "value": self.safe_length(out)

        })

        relations.append({

            "relation": "size_difference",

            "value": (

                self.safe_length(out)

                -

                self.safe_length(inp)

            )

        })

        relations.append({

            "relation": "size_preserved",

            "value": (

                self.safe_length(inp)

                ==

                self.safe_length(out)

            )

        })

        # -------------------------------------------------
        # Numeric relation
        # -------------------------------------------------

        if isinstance(inp, (int, float)) and isinstance(out, (int, float)):

            relations.extend(

                self.numeric_relations(

                    inp,

                    out

                )

            )

        # -------------------------------------------------
        # Sequence relation
        # -------------------------------------------------

        elif isinstance(inp, (list, tuple, set)) and isinstance(

            out,

            (list, tuple, set)

        ):

            relations.extend(

                self.sequence_relations(

                    list(inp),

                    list(out)

                )

            )

        # -------------------------------------------------
        # Dictionary relation
        # -------------------------------------------------

        elif isinstance(inp, dict) and isinstance(out, dict):

            relations.extend(

                self.dictionary_relations(

                    inp,

                    out

                )

            )

        # -------------------------------------------------
        # Generic mapping
        # -------------------------------------------------

        else:

            relations.append({

                "relation": "mapping",

                "input": inp,

                "output": out

            })

        return relations

    # =====================================================
    # Sequence Relations
    # =====================================================

    def sequence_relations(

        self,

        inp,

        out

    ):

        relations = []

        relations.append({

            "relation": "length_preserved",

            "value": len(inp) == len(out)

        })

        relations.append({

            "relation": "elements_preserved",

            "value": Counter(inp) == Counter(out)

        })

        relations.append({

            "relation": "same_multiset",

            "value": Counter(inp) == Counter(out)

        })

        relations.append({

            "relation": "order_changed",

            "value": inp != out

        })

        relations.append({

            "relation": "order_preserved",

            "value": inp == out

        })

        relations.append({

            "relation": "input_unique",

            "value": len(inp) == len(set(inp))

        })

        relations.append({

            "relation": "output_unique",

            "value": len(out) == len(set(out))

        })

        relations.append({

            "relation": "duplicate_count_preserved",

            "value":

                (len(inp)-len(set(inp)))

                ==

                (len(out)-len(set(out)))

        })
                # -------------------------------------------------
        # Reverse Detection
        # -------------------------------------------------

        relations.append({

            "relation": "reverse_detected",

            "value": out == list(reversed(inp))

        })

        # -------------------------------------------------
        # Rotation Detection
        # -------------------------------------------------

        rotation = self.rotation_amount(inp, out)

        relations.append({

            "relation": "rotation_detected",

            "value": rotation != -1

        })

        relations.append({

            "relation": "rotation_amount",

            "value": rotation

        })

        # -------------------------------------------------
        # Stable Partition Detection
        # -------------------------------------------------

        stable_partition = self.is_stable_partition(inp, out)

        relations.append({

            "relation": "stable_partition",

            "value": stable_partition

        })

        # -------------------------------------------------
        # Even / Odd Partition
        # -------------------------------------------------

        relations.append({

            "relation": "evens_before_odds",

            "value": self.evens_before_odds(out)

        })

        relations.append({

            "relation": "odds_before_evens",

            "value": self.odds_before_evens(out)

        })

        # -------------------------------------------------
        # Prefix Preservation
        # -------------------------------------------------

        relations.append({

            "relation": "prefix_preserved",

            "value": self.common_prefix(inp, out)

        })

        # -------------------------------------------------
        # Suffix Preservation
        # -------------------------------------------------

        relations.append({

            "relation": "suffix_preserved",

            "value": self.common_suffix(inp, out)

        })

        # -------------------------------------------------
        # Sorting Detection
        # -------------------------------------------------

        relations.append({

            "relation": "sorted_ascending",

            "value": out == sorted(out)

        })

        relations.append({

            "relation": "sorted_descending",

            "value": out == sorted(out, reverse=True)

        })

        # -------------------------------------------------
        # Duplicate Removal
        # -------------------------------------------------

        relations.append({

            "relation": "duplicates_removed",

            "value":

                len(set(inp))

                ==

                len(out)

                and

                len(inp) >= len(out)

        })

        # -------------------------------------------------
        # Numeric Sequence Relations
        # -------------------------------------------------

        if all(

            isinstance(x, (int, float))

            for x in inp + out

        ):

            relations.append({

                "relation": "sum_preserved",

                "value":

                    sum(inp)

                    ==

                    sum(out)

            })

            relations.append({

                "relation": "minimum_preserved",

                "value":

                    min(inp)

                    ==

                    min(out)

            })

            relations.append({

                "relation": "maximum_preserved",

                "value":

                    max(inp)

                    ==

                    max(out)

            })

        # -------------------------------------------------
        # Position Mapping
        # -------------------------------------------------

        for index, value in enumerate(inp):

            if value in out:

                relations.append({

                    "relation": "position_mapping",

                    "value": value,

                    "input_position": index,

                    "output_position": out.index(value)

                })

        # -------------------------------------------------
        # Removed Elements
        # -------------------------------------------------

        for value in inp:

            if value not in out:

                relations.append({

                    "relation": "removed_element",

                    "value": value

                })

        # -------------------------------------------------
        # Added Elements
        # -------------------------------------------------

        for value in out:

            if value not in inp:

                relations.append({

                    "relation": "added_element",

                    "value": value

                })

        return relations

            # =====================================================
    # Numeric Relations
    # =====================================================

    def numeric_relations(self, inp, out):

        relations = []

        relations.append({

            "relation": "difference",

            "value": out - inp

        })

        relations.append({

            "relation": "absolute_difference",

            "value": abs(out - inp)

        })

        relations.append({

            "relation": "greater_than",

            "value": out > inp

        })

        relations.append({

            "relation": "less_than",

            "value": out < inp

        })

        relations.append({

            "relation": "equal",

            "value": out == inp

        })

        if inp != 0:

            relations.append({

                "relation": "ratio",

                "value": out / inp

            })

        # Detect simple arithmetic transformations

        if out == inp + 1:

            relations.append({

                "relation": "increment",

                "value": 1

            })

        if out == inp - 1:

            relations.append({

                "relation": "decrement",

                "value": 1

            })

        if out == inp * 2:

            relations.append({

                "relation": "double",

                "value": True

            })

        if out == inp / 2:

            relations.append({

                "relation": "half",

                "value": True

            })

        if out == inp * inp:

            relations.append({

                "relation": "square",

                "value": True

            })

        return relations

    # =====================================================
    # Dictionary Relations
    # =====================================================

    def dictionary_relations(self, inp, out):

        relations = []

        input_keys = set(inp.keys())
        output_keys = set(out.keys())

        relations.append({

            "relation": "shared_keys",

            "value": sorted(input_keys & output_keys)

        })

        relations.append({

            "relation": "removed_keys",

            "value": sorted(input_keys - output_keys)

        })

        relations.append({

            "relation": "added_keys",

            "value": sorted(output_keys - input_keys)

        })

        relations.append({

            "relation": "key_count_preserved",

            "value": len(input_keys) == len(output_keys)

        })

        for key in input_keys & output_keys:

            relations.append({

                "relation": "field_mapping",

                "field": key,

                "input": inp[key],

                "output": out[key],

                "same_value": inp[key] == out[key]

            })

        return relations

    # =====================================================
    # Rotation Detection
    # =====================================================

    def rotation_amount(self, inp, out):

        if len(inp) != len(out):
            return -1

        n = len(inp)

        for i in range(n):

            if inp[i:] + inp[:i] == out:
                return i

        return -1

    # =====================================================
    # Stable Partition Detection
    # =====================================================

    def is_stable_partition(self, inp, out):

        if not all(isinstance(x, int) for x in inp):
            return False

        evens = [x for x in inp if x % 2 == 0]
        odds = [x for x in inp if x % 2 == 1]

        return out == evens + odds

    # =====================================================
    # Prefix Preservation
    # =====================================================

    def common_prefix(self, inp, out):

        count = 0

        for a, b in zip(inp, out):

            if a == b:
                count += 1
            else:
                break

        return count

    # =====================================================
    # Suffix Preservation
    # =====================================================

    def common_suffix(self, inp, out):

        count = 0

        for a, b in zip(reversed(inp), reversed(out)):

            if a == b:
                count += 1
            else:
                break

        return count

        # =====================================================
    # Even Before Odd Detection
    # =====================================================

    def evens_before_odds(self, seq):

        if not seq:
            return False

        if not all(isinstance(x, int) for x in seq):
            return False

        seen_odd = False

        for value in seq:

            if value % 2 == 1:
                seen_odd = True

            elif seen_odd:
                return False

        return True

    # =====================================================
    # Odd Before Even Detection
    # =====================================================

    def odds_before_evens(self, seq):

        if not seq:
            return False

        if not all(isinstance(x, int) for x in seq):
            return False

        seen_even = False

        for value in seq:

            if value % 2 == 0:
                seen_even = True

            elif seen_even:
                return False

        return True

    # =====================================================
    # Same Structure
    # =====================================================

    def same_structure(self, a, b):

        if type(a) != type(b):
            return False

        if isinstance(a, dict):

            return set(a.keys()) == set(b.keys())

        if isinstance(a, (list, tuple, set)):

            return len(a) == len(b)

        return True

    # =====================================================
    # Safe Length
    # =====================================================

    def safe_length(self, obj):

        try:
            return len(obj)

        except Exception:
            return 1

    # =====================================================
    # Utility : Check Numeric Sequence
    # =====================================================

    def is_numeric_sequence(self, seq):

        return all(

            isinstance(x, (int, float))

            for x in seq

        )

    # =====================================================
    # Utility : Check Sorted
    # =====================================================

    def is_sorted_ascending(self, seq):

        try:
            return seq == sorted(seq)
        except Exception:
            return False

    # =====================================================
    # Utility : Check Reverse Sorted
    # =====================================================

    def is_sorted_descending(self, seq):

        try:
            return seq == sorted(seq, reverse=True)
        except Exception:
            return False

    # =====================================================
    # Utility : Duplicate Count
    # =====================================================

    def duplicate_count(self, seq):

        try:
            return len(seq) - len(set(seq))
        except Exception:
            return 0

    # =====================================================
    # Utility : Frequency Equality
    # =====================================================

    def same_frequency(self, inp, out):

        try:
            return Counter(inp) == Counter(out)
        except Exception:
            return False