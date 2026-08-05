"""
=========================================================
Generic DeepProbLog Model
=========================================================

Acts as a lightweight wrapper around the symbolic and
neural components.

No task-specific implementation is included.

=========================================================
"""

from deepproblog.neural_interface import NeuralInterface


class DeepProbLogModel:

    def __init__(self):

        self.interface = NeuralInterface()

    # =====================================================

    def train(self, dataset):

        print("\nDeepProbLog training initialized.")
        print(f"Training examples : {len(dataset)}")

    # =====================================================

    def infer(self, example):

        prediction = self.interface.predict(

            example.example_id

        )

        return {

            "prediction": prediction,

            "confidence": 1.0 if prediction is not None else 0.0

        }

    # =====================================================

    def explain(self):

        return "Inference performed using the Neuro-Symbolic reasoning pipeline."