"""
=========================================================
Neural Interface
=========================================================

Provides a generic interface between neural predictions
and symbolic reasoning.

The interface is intentionally algorithm-independent.

=========================================================
"""


class NeuralInterface:

    def __init__(self):

        self.predictions = {}

    # =====================================================

    def register(self, example_id, prediction):

        self.predictions[example_id] = prediction

    # =====================================================

    def predict(self, example_id):

        return self.predictions.get(example_id)

    # =====================================================

    def clear(self):

        self.predictions.clear()