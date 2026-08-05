"""
============================================================
Common Data Models
============================================================
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TrainingExample:
    """
    Universal training example.
    """

    example_id: int

    input_data: Any

    output_data: Any

    context: Optional[Any] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {

            "example_id": self.example_id,

            "input_data": self.input_data,

            "output_data": self.output_data,

            "context": self.context,

            "metadata": self.metadata

        }

    def copy(self):

        return TrainingExample(

            example_id=self.example_id,

            input_data=self.input_data,

            output_data=self.output_data,

            context=self.context,

            metadata=dict(self.metadata)

        )

    def __repr__(self):

        return (

            f"\nExample {self.example_id}\n"

            f"Input    : {self.input_data}\n"

            f"Output   : {self.output_data}\n"

            f"Context  : {self.context}\n"

            f"Metadata : {self.metadata}"

        )


@dataclass
class KnowledgeObject:
    """
    Knowledge representation for one example.
    """

    example: TrainingExample

    facts: list = field(default_factory=list)

    properties: dict = field(default_factory=dict)

    relations: list = field(default_factory=list)

    features: dict = field(default_factory=dict)


@dataclass
class Hypothesis:

    hypothesis_id: int

    description: str

    predicates: list = field(default_factory=list)

    rules: list = field(default_factory=list)

    confidence: float = 0.0

    support: int = 0

    coverage: float = 0.0

    ranking_score: float = 0.0

    verified: bool = False


@dataclass
class ExecutionResult:

    input_data: Any

    predicted_output: Any

    confidence: float

    execution_time: float

    status: str

    explanation: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)