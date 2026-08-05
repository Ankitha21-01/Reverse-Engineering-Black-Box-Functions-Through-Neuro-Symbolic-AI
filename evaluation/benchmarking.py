"""
=========================================================
Universal Benchmarking
=========================================================

Collects execution statistics across multiple runs.

=========================================================
"""

import statistics


class Benchmark:

    def __init__(self):

        self.history = []

    # =====================================================

    def add(self, metrics):

        self.history.append(metrics)

    # =====================================================

    def summary(self):

        if not self.history:

            return {}

        times = [

            h["execution_time"]

            for h in self.history

        ]

        success = [

            h["success"]

            for h in self.history

        ]

        return {

            "runs": len(self.history),

            "average_time": round(

                statistics.mean(times),

                6

            ),

            "minimum_time": round(

                min(times),

                6

            ),

            "maximum_time": round(

                max(times),

                6

            ),

            "success_rate": round(

                sum(success) / len(success),

                3

            )

        }

    # =====================================================

    def print(self):

        report = self.summary()

        if not report:

            print("No benchmark results.")

            return

        print("\n" + "=" * 60)

        print("BENCHMARK REPORT")

        print("=" * 60)

        for key, value in report.items():

            print(f"{key:20}: {value}")