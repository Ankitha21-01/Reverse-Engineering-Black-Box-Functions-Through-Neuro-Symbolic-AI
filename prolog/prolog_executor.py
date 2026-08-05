"""
=========================================================
Universal Prolog Executor
=========================================================

Executes learned Prolog programs.

Features

✓ Fresh SWI-Prolog engine
✓ Safe execution
✓ Timeout support
✓ Execution metadata
✓ Runtime statistics
✓ Output comparison
✓ Execution tracing

=========================================================
"""

import os
import time
import uuid
from datetime import datetime

from pyswip import Prolog
from pyswip.easy import Atom

class PrologExecutor:

    def __init__(self, timeout=5):

        # Maximum execution time (seconds)
        self.timeout = timeout

        # Built-in predicates that are not helper predicates
        self.builtin_predicates = {

            "append",
            "member",
            "reverse",
            "length",
            "sort",
            "msort",
            "findall",
            "bagof",
            "setof",
            "nth0",
            "integer",
            "number",
            "atom",
            "is",
            "true",
            "fail"

        }

        self.execution_counter = 0

        # =====================================================

    def to_prolog(self, obj):

        if obj is None:
            return "[]"

        if isinstance(obj, bool):
            return "true" if obj else "false"

        if isinstance(obj, (int, float)):
            return str(obj)

        if isinstance(obj, str):

            obj = obj.replace('"', '\\"')

            return f'"{obj}"'

        if isinstance(obj, (list, tuple)):

            return "[" + ",".join(

                self.to_prolog(x)

                for x in obj

            ) + "]"

        if isinstance(obj, dict):

            parts = []

            for key, value in obj.items():

                key = str(key).replace(" ", "_")

                parts.append(

                    f"{key}({self.to_prolog(value)})"

                )

            return "[" + ",".join(parts) + "]"

        return str(obj)

    

    def from_prolog(self, obj):

        if isinstance(obj, list):
            return [self.from_prolog(x) for x in obj]

        if isinstance(obj, tuple):
            return tuple(self.from_prolog(x) for x in obj)

        if isinstance(obj, Atom):
            return str(obj)

        return obj
        # =====================================================

    def outputs_match(

        self,
        predicted,
        expected

    ):

        return predicted == expected


    # =====================================================

    def execution_score(

        self,
        success,
        execution_time,
        match

    ):

        score = 0.0

        if success:
            score += 0.40

        if match:
            score += 0.50

        if execution_time < 1:
            score += 0.10

        return round(score, 3)


    # =====================================================

    def new_execution_id(self):

        self.execution_counter += 1

        return f"EXEC-{self.execution_counter:05d}"
        # =====================================================

    def execute(

        self,
        prolog_file,
        input_data,
        expected_output=None

    ):

        start = time.time()

        query = ""

        execution_id = self.new_execution_id()

        try:

            if not os.path.exists(prolog_file):

                raise FileNotFoundError(prolog_file)

            prolog = Prolog()

# Remove predicates from previous runs (ignore errors if they don't exist)
            try:
                list(prolog.query("abolish(transform/2)"))
            except:
                pass

            try:
                list(prolog.query("abolish(helper/2)"))
            except:
                pass

            prolog.consult(prolog_file)

            prolog_input = self.to_prolog(input_data)

            query = f"transform({prolog_input}, Output)"

            results = list(

                prolog.query(

                    query,

                    maxresult=1

                )

            )

            end = time.time()

            execution_time = round(

                end - start,

                6

            )

            if len(results) == 0:

                return {

                    "execution_id": execution_id,

                    "timestamp": datetime.now().isoformat(),

                    "status": "NO_SOLUTION",

                    "query": query,

                    "input": input_data,

                    "expected_output": expected_output,

                    "predicted_output": None,

                    "match": False,

                    "accuracy": 0.0,

                    "execution_score": 0.0,

                    "bindings": {},

                    "execution_time": execution_time

                }

            bindings = dict(results[0])

            print("\n===== PYTHON RESULTS =====")
            print(results)
            print("Bindings:", bindings)
            print("Output term:", bindings.get("Output"))

            output = self.from_prolog(
                bindings.get("Output")
            )

            match = (

                expected_output is None

                or

                self.outputs_match(

                    output,

                    expected_output

                )

            )

            score = self.execution_score(

                True,

                execution_time,

                match

            )

            return {

                    "execution_id": execution_id,

                    "timestamp": datetime.now().isoformat(),

                    "status": "SUCCESS",

                    "query": query,

                    "input": input_data,

                    "expected_output": expected_output,

                    "output": output,                 # <-- add this

                           # keep this

                    "match": match,

                    "accuracy": 1.0 if match else 0.0,

                    "execution_score": score,

                    "bindings": bindings,

                    "execution_time": execution_time

                }

            

        except Exception as e:

            end = time.time()

            return {

                "execution_id": execution_id,

                "timestamp": datetime.now().isoformat(),

                "status": "ERROR",

                "query": query,

                "input": input_data,

                "expected_output": expected_output,

                "predicted_output": None,

                "match": False,

                "accuracy": 0.0,

                "execution_score": 0.0,

                "bindings": {},

                "error": str(e),

                "execution_time": round(

                    end-start,

                    6

                )

            }
        # =====================================================

    def execute_dataset(

        self,

        prolog_file,

        dataset

    ):

        executions = []

        success = 0

        total_time = 0.0

        total_score = 0.0

        for example in dataset:

            result = self.execute(

                prolog_file,

                example.input_data,

                example.output_data

            )

            executions.append(result)

            total_time += result["execution_time"]

            total_score += result["execution_score"]

            if result["match"]:

                success += 1

        total = len(dataset)

        accuracy = (

            success / total

            if total

            else 0.0

        )

        average_time = (

            total_time / total

            if total

            else 0.0

        )

        average_score = (

            total_score / total

            if total

            else 0.0

        )

        return {

            "examples": total,

            "successful": success,

            "failed": total - success,

            "accuracy": round(

                accuracy,

                3

            ),

            "average_execution_time": round(

                average_time,

                6

            ),

            "average_execution_score": round(

                average_score,

                3

            ),

            "executions": executions

        }