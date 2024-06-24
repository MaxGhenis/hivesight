from typing import Dict, List, Optional
from config import LIKERT_LABELS


def create_prompt(
    persona: Dict,
    statement: str,
    question_type: str,
    choices: Optional[List[str]] = None,
) -> str:
    persona_info = f"You are roleplaying as a {persona['age']}-year-old from {persona['state']} with annual income of ${persona['income']}."
    general_instructions = "Respond to the following question based on this persona's likely perspective, beliefs, and experiences."

    if question_type == "likert":
        likert_scale = ", ".join(
            [f"{i+1} = {label}" for i, label in enumerate(LIKERT_LABELS)]
        )
        return f"""{persona_info}
        {general_instructions}
        Use a 5-point scale where {likert_scale}.
        Statement: "{statement}"
        How much do you agree with the statement?
        Respond with ONLY a single number from 1 to 5, no additional explanation."""

    elif question_type == "multiple_choice":
        if choices is None:
            raise ValueError(
                "Choices must be provided for multiple choice questions."
            )
        numbered_choices = "\n".join(
            [f"{i+1}. {choice}" for i, choice in enumerate(choices)]
        )
        return f"""{persona_info}
        {general_instructions}
        Question: "{statement}"
        Choose from the following options:
        {numbered_choices}
        Respond with ONLY the single number of your chosen option (1, 2, 3, etc.), nothing else. Do not include the choice text or any explanation."""

    else:
        raise ValueError(
            "Unsupported question type. Supported types are 'likert' and 'multiple_choice'."
        )
