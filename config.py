import os
import numpy as np

API_KEYS = {
    "OPENAI": os.getenv("OPENAI_API_KEY"),
    "ANTHROPIC": os.getenv("ANTHROPIC_API_KEY"),
}

MODEL_MAP = {
    "GPT-3.5": "gpt-3.5-turbo",
    "GPT-4o": "gpt-4o",
}

AGE_BINS = [0, 18, 25, 35, 45, 55, 65, np.inf]
INCOME_BINS = [0, 30000, 60000, 90000, 120000, np.inf]

LIKERT_LABELS = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree",
]

LIKERT_COLORS = {
    "Strongly Disagree": "#5A5A5A",  # Dark gray
    "Disagree": "#BFBFBF",  # Light gray
    "Neutral": "#F5F5F5",  # Very light gray
    "Agree": "#FFD700",  # Golden yellow
    "Strongly Agree": "#B8860B",  # Dark goldenrod
}
