import plotly.graph_objects as go
from typing import List
import pandas as pd
from config import LIKERT_LABELS, LIKERT_COLORS


def create_enhanced_visualizations(
    response_counts: pd.DataFrame, pivot: pd.DataFrame, groupby_var: str
) -> List[go.Figure]:
    figures = []

    # Distribution of scores as horizontal stacked bar chart
    fig1 = go.Figure()
    for label in LIKERT_LABELS:
        count = response_counts.loc[
            response_counts["likert_label"] == label, "percentage"
        ]
        fig1.add_trace(
            go.Bar(
                y=["Distribution of Responses"],
                x=[count.values[0] if not count.empty else 0],
                name=label,
                orientation="h",
                marker=dict(color=LIKERT_COLORS[label]),
                text=[f"{count.values[0]:.2%}"] if not count.empty else ["0%"],
                textposition="inside",
            )
        )
    fig1.update_layout(
        barmode="stack",
        title="Distribution of Responses",
        xaxis_title="Percentage",
        yaxis_title="Likert Score",
        height=300,  # Adjust height to make it shorter
        yaxis=dict(
            showticklabels=False
        ),  # Hide y-axis tick labels for a cleaner look
    )
    figures.append(fig1)

    # Likert scale results by groupby variable
    fig2 = go.Figure()
    for label in LIKERT_LABELS:
        fig2.add_trace(
            go.Bar(
                y=pivot[groupby_var].astype(str),
                x=pivot[label],
                name=label,
                orientation="h",
                marker=dict(color=LIKERT_COLORS[label]),
                text=[f"{val:.2%}" for val in pivot[label]],
                textposition="inside",
            )
        )
    fig2.update_layout(
        barmode="stack",
        title=f"Likert Scale Results by {groupby_var.capitalize()} Group",
        xaxis_title="Percentage",
        yaxis_title=f"{groupby_var.capitalize()} Group",
        height=300,  # Adjust height to make it shorter
    )
    figures.append(fig2)

    return figures
