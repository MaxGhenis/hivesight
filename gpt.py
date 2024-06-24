import os
from openai import OpenAI, AsyncOpenAI, NOT_GIVEN as OPENAI_NOT_GIVEN
import streamlit as st
from config import MODEL_MAP

openai_api_key = os.getenv("OPENAI_API_KEY", st.secrets["OPENAI_API_KEY"])

openai_client = OpenAI()
openai_client_async = AsyncOpenAI()

EXPLANATION_APPEND = " Please provide an explanation."


def query_openai_batch(
    prompts,
    model_type,
    temperature=1.0,
    top_p=None,
    system_prompt=None,
    max_tokens=None,
):
    responses = []
    for prompt in prompts:
        response = query_openai(
            prompt,
            model_type,
            False,
            1,
            temperature,
            top_p,
            system_prompt,
            max_tokens,
        )
        responses.extend(response)
    return responses


def query_openai(
    question,
    model_type,
    request_explanation,
    num_queries,
    temperature=1.0,
    top_p=None,
    system_prompt=None,
    max_tokens=None,
):
    top_p_input = OPENAI_NOT_GIVEN if top_p is None else top_p

    if not question:
        print("Error: Empty question provided")
        return ["Error: Empty question"]

    try:
        user_prompt = question
        if request_explanation:
            user_prompt = f"{user_prompt} {EXPLANATION_APPEND}"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        if model_type == "Claude-3":
            from anthropic import Anthropic

            anthropic_client = Anthropic(
                api_key=os.getenv(
                    "ANTHROPIC_API_KEY", st.secrets["ANTHROPIC_API_KEY"]
                )
            )
            response = anthropic_client.messages.create(
                model=MODEL_MAP[model_type],
                max_tokens=max_tokens or 500,
                temperature=temperature,
                messages=messages,
            )
            return [response.content[0].text.strip()]
        else:
            response = openai_client.chat.completions.create(
                model=MODEL_MAP[model_type],
                temperature=temperature,
                top_p=top_p_input,
                messages=messages,
                max_tokens=max_tokens or 500,
                n=num_queries,
            )
            return [r.message.content.strip() for r in response.choices]
    except Exception as e:
        print(f"Error during API call for model {model_type}:", e)
        return [f"Error: {str(e)}"]
