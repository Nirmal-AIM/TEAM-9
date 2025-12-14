"""
Configuration file for ML Pipeline
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Dataset
CSV_FILE_PATH = BASE_DIR.parent / "public" / "credit_score.csv"

# Model parameters
CREDIT_SCORE_MIN = 300
CREDIT_SCORE_MAX = 900
TEST_SIZE = 0.2
RANDOM_STATE = 42

# User categories based on credit score
CREDIT_CATEGORIES = {
    "Excellent": (750, 900),
    "Good": (700, 749),
    "Fair": (650, 699),
    "Poor": (600, 649),
    "Very Poor": (300, 599)
}

