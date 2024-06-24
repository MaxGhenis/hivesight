from typing import List, Dict, Tuple
import streamlit as st
from data_handling import select_diverse_personas
from prompts import create_prompt
from gpt import query_openai_batch
from scipy import stats
import pandas as pd


def parse_numeric_response(response, max_value):
    try:
        score = int(response.strip())
        if 1 <= score <= max_value:
            return score
    except ValueError:
        pass
    return None


def batch_simulate_responses(
    statement: str,
    choices: List[str],
    num_queries: int,
    model_type: str,
    age_range: Tuple[int, int],
    income_range: Tuple[float, float],
    question_type: str,
) -> List[Dict]:
    personas = select_diverse_personas(num_queries, age_range, income_range)
    prompts = [
        create_prompt(persona, statement, question_type, choices)
        for persona in personas
    ]

    # Split prompts into batches of 20 (or adjust based on API limits)
    batch_size = 20
    batched_prompts = [
        prompts[i : i + batch_size] for i in range(0, len(prompts), batch_size)
    ]

    all_responses = []
    for batch in batched_prompts:
        responses = query_openai_batch(
            batch, model_type, max_tokens=1
        )  # Limit to 1 token
        all_responses.extend(responses)

    valid_responses = []
    for persona, response in zip(personas, all_responses):
        if response.startswith("Error"):
            st.warning(f"API Error: {response}")
            continue
        if question_type == "likert":
            score = parse_numeric_response(response, 5)
            if score is not None:
                valid_responses.append(
                    {
                        "persona": f"{persona['age']}-year-old from {persona['state']} with annual income of ${persona['income']}",
                        "age": persona["age"],
                        "income": persona["income"],
                        "state": persona["state"],
                        "score": score,
                        "original_response": response,
                    }
                )
        else:  # multiple choice
            try:
                choice_index = int(response.strip()) - 1
                if 0 <= choice_index < len(choices):
                    valid_responses.append(
                        {
                            "persona": f"{persona['age']}-year-old from {persona['state']} with annual income of ${persona['income']}",
                            "age": persona["age"],
                            "income": persona["income"],
                            "state": persona["state"],
                            "choice": choices[choice_index],
                            "original_response": response,
                        }
                    )
                else:
                    st.warning(f"Invalid choice index: {response}")
            except ValueError:
                st.warning(f"Invalid response for multiple choice: {response}")

    return valid_responses


def analyze_responses(responses: List[Dict], question_type: str) -> Dict:
    if not responses:
        return {"count": 0}

    df = pd.DataFrame(responses)

    if question_type == "likert":
        analysis = {
            "mean": df["score"].mean(),
            "median": df["score"].median(),
            "std_dev": df["score"].std(),
            "count": df["score"].count(),
        }

        # Calculate confidence interval
        try:
            n = len(df)
            sem = stats.sem(df["score"])
            ci = stats.t.interval(
                confidence=0.95, df=n - 1, loc=analysis["mean"], scale=sem
            )
            analysis["confidence_interval"] = ci
        except Exception as e:
            st.warning(f"Error calculating confidence interval: {str(e)}")
            analysis["confidence_interval"] = (None, None)

    else:  # multiple choice
        if "choice" not in df.columns:
            return {"count": 0, "error": "No valid choices found in responses"}
        analysis = df["choice"].value_counts(normalize=True).to_dict()
        analysis["count"] = len(df)

    return analysis
