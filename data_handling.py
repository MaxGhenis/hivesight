import pandas as pd
from typing import Tuple, List
import streamlit as st


@st.cache_data
def load_perspectives_data() -> pd.DataFrame:
    return pd.read_csv("perspectives.csv")


perspectives_data = load_perspectives_data()


def select_diverse_personas(
    num_queries: int,
    age_range: Tuple[int, int],
    income_range: Tuple[float, float],
) -> List[dict]:
    filtered_data = perspectives_data[
        (perspectives_data["age"] >= age_range[0])
        & (perspectives_data["age"] <= age_range[1])
        & (perspectives_data["income"] >= income_range[0])
        & (perspectives_data["income"] <= income_range[1])
    ]
    return filtered_data.sample(
        n=min(num_queries, len(filtered_data)), weights="weight"
    ).to_dict("records")
