"""
=========================================================
Universal Knowledge Generator
=========================================================

Generates a complete symbolic knowledge representation
for every training example.

Knowledge consists of

✓ Facts
✓ Properties
✓ Relations
✓ Features

This module is completely domain independent.

=========================================================
"""

from knowledge.facts import FactGenerator
from knowledge.property_discovery import PropertyDiscovery
from knowledge.relation_discovery import RelationDiscovery
from knowledge.feature_extractor import FeatureExtractor

from utils.models import KnowledgeObject


class KnowledgeGenerator:

    def __init__(self):

        self.fact_generator = FactGenerator()

        self.property_generator = PropertyDiscovery()

        self.relation_generator = RelationDiscovery()

        self.feature_extractor = FeatureExtractor()

    # =====================================================

    def generate(self, dataset):

        knowledge_base = []

        for example in dataset:

            facts = self.fact_generator.generate(
                example
            )

            properties = self.property_generator.discover(
                example
            )

            relations = self.relation_generator.discover(
                example
            )

            features = self.feature_extractor.extract(
                example
            )

            knowledge = KnowledgeObject(

                example=example,

                facts=facts,

                properties=properties,

                relations=relations,

                features=features

            )

            knowledge_base.append(knowledge)

        return knowledge_base

    # =====================================================

    def summary(self, knowledge_base):

        summary = {

            "examples": len(knowledge_base),

            "facts": 0,

            "relations": 0,

            "properties": 0,

            "features": 0

        }

        for item in knowledge_base:

            summary["facts"] += len(item.facts)

            summary["relations"] += len(item.relations)

            summary["properties"] += len(item.properties)

            summary["features"] += len(item.features)

        return summary

    # =====================================================

    def print_summary(self, knowledge_base):

        summary = self.summary(knowledge_base)

        print("\n" + "=" * 70)
        print("KNOWLEDGE BASE SUMMARY")
        print("=" * 70)

        print("Training Examples :", summary["examples"])

        print("Facts             :", summary["facts"])

        print("Relations         :", summary["relations"])

        print("Properties        :", summary["properties"])

        print("Features          :", summary["features"])

        print("=" * 70)

    # =====================================================

    def print_example(self, knowledge):

        print("\nExample :", knowledge.example.example_id)

        print("-" * 60)

        print("\nFacts")

        for fact in knowledge.facts:

            print(" ", fact)

        print("\nProperties")

        for key, value in knowledge.properties.items():

            print(f" {key:30}: {value}")

        print("\nRelations")

        for relation in knowledge.relations:

            print(" ", relation)

        print("\nFeatures")

        for key, value in knowledge.features.items():

            print(f" {key:30}: {value}")

        print("=" * 70)