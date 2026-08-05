"""
============================================================
Configuration File
Human-in-the-Loop Neuro-Symbolic AI Framework
============================================================
"""

import os

# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
REPORT_DIR = os.path.join(GENERATED_DIR, "reports")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ----------------------------------------------------------
# Dataset
# ----------------------------------------------------------

INPUT_CSV = os.path.join(DATA_DIR, "input.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "output.csv")

# ----------------------------------------------------------
# Generated Files
# ----------------------------------------------------------

PROLOG_FILE = os.path.join(GENERATED_DIR, "rules.pl")

# ----------------------------------------------------------
# LLM Configuration
# ----------------------------------------------------------

GROQ_API_KEY = ""

# Best reasoning model currently available in your project
MODEL_NAME = "llama-3.3-70b-versatile"

TEMPERATURE = 0.0

MAX_TOKENS = 4096

TOP_P = 1.0

# ----------------------------------------------------------
# DeepProbLog
# ----------------------------------------------------------

DEEPPROBLOG_MODEL = os.path.join(
    GENERATED_DIR,
    "deepproblog_model.pt"
)

VERIFY_THRESHOLD = 0.70

# ----------------------------------------------------------
# ILP
# ----------------------------------------------------------

MIN_SUPPORT = 2

MIN_CONFIDENCE = 0.60

MIN_COVERAGE = 0.50

MAX_HYPOTHESES = 10

# ----------------------------------------------------------
# Human Feedback
# ----------------------------------------------------------

ENABLE_HUMAN_FEEDBACK = True

MAX_ITERATIONS = 5

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

LOG_LEVEL = "INFO"

SAVE_REPORT = True

SAVE_PROLOG = True

# ----------------------------------------------------------
# Execution
# ----------------------------------------------------------

EXECUTION_TIMEOUT = 30

ALLOW_FALLBACK_REASONING = True