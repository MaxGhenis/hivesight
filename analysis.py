import pandas as pd
from typing import List, Dict
from config import LIKERT_LABELS, AGE_BINS, INCOME_BINS
import numpy as np


def analyze_responses(responses: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(responses)

    # Likert scale mapping
    likert_mapping = {i + 1: LIKERT_LABELS[i] for i in range(5)}
    df["likert_label"] = df["score"].map(likert_mapping)

    # Calculate the percentage of total responses for each Likert label
    response_counts = (
        df["likert_label"].value_counts(normalize=True).reset_index()
    )
    response_counts.columns = ["likert_label", "percentage"]

    return response_counts


def create_pivot_table(df: pd.DataFrame, groupby_var: str) -> pd.DataFrame:
    if groupby_var == "age":
        bins = AGE_BINS
    elif groupby_var == "income":
        bins = INCOME_BINS
    else:
        raise ValueError(
            "Unsupported groupby variable. Supported variables are 'age' and 'income'."
        )

    labels = generate_labels(bins)

    pivot = (
        df.pivot_table(
            values="score",
            index=pd.cut(df[groupby_var], bins=bins, labels=labels),
            columns="likert_label",
            aggfunc="count",
            fill_value=0,
        )
        .apply(lambda x: x / x.sum(), axis=1)
        .reset_index()
    )

    return pivot


def generate_labels(bins):
    labels = []
    for i in range(len(bins) - 1):
        if bins[i + 1] == np.inf:
            labels.append(f"{bins[i]}+")
        else:
            labels.append(f"{bins[i]}-{bins[i + 1] - 1}")
    return labels
