import streamlit as st
from anthropic import Anthropic, AsyncAnthropic
import os
from scipy.stats import beta
import time
import pandas as pd
from custom_components import download_button
import asyncio

# Assuming API key and client setup
api_key = os.getenv("ANTHROPIC_API_KEY", st.secrets["ANTHROPIC_API_KEY"])
client = Anthropic(api_key=api_key)
client_async = AsyncAnthropic(api_key=api_key)


def query_claude(question, model_type, request_explanation):
    model_map = {
        "Haiku": "claude-3-haiku-20240307",
        "Sonnet": "claude-3-sonnet-20240229",
        "Opus": "claude-3-opus-20240229",
    }
    try:
        if request_explanation:
            prompt = f"{question} Begin your response with 'yes' or 'no', and then provide an explanation."
        else:
            prompt = f"{question} Do not reply with anything other than 'yes' or 'no'."

        response = client.messages.create(
            max_tokens=500,
            model=model_map[model_type],
            messages=[{"role": "user", "content": prompt}],
        )
        if (
            response.content
            and isinstance(response.content, list)
            and hasattr(response.content[0], "text")
        ):
            return response.content[0].text.strip()
    except Exception as e:
        print("Error during API call:", e)
    return "Error or no data"


async def query_claude_async(question, model_type, request_explanation, num_queries):
    model_map = {
        "Haiku": "claude-3-haiku-20240307",
        "Sonnet": "claude-3-sonnet-20240229",
        "Opus": "claude-3-opus-20240229",
    }
    try:
        if request_explanation:
            prompt = f"{question} Begin your response with 'yes' or 'no', and then provide an explanation."
        else:
            prompt = f"{question} Do not reply with anything other than 'yes' or 'no'."

        async def send_message_async(content):
            response = await client_async.messages.create(
                model=model_map[model_type],
                max_tokens=500,
                messages=[{"role": "user", "content": content}]
            )
            return response

        response = await asyncio.gather(*[send_message_async(prompt) for _ in range(num_queries)])
        if (
            response[0].content
            and isinstance(response[0].content, list)
            and hasattr(response[0].content[0], "text")
        ):
            return [r.content[0].text.strip() for r in response]
    except Exception as e:
        print("Error during API call:", e)
    return "Error or no data"


def is_valid_response(response, request_explanation):
    if request_explanation:
        return response.lower().startswith(
            "yes"
        ) or response.lower().startswith("no")
    else:
        return response.lower() in ["yes", "no"]


def summarize_explanations(explanations):
    summary_prompt = (
        "Please provide a concise summary of the main points from the following explanations:\n\n"
        + "\n".join(explanations)
    )
    response = client.messages.create(
        max_tokens=200,
        model="claude-3-opus-20240229",
        messages=[{"role": "user", "content": summary_prompt}],
    )
    if (
        response.content
        and isinstance(response.content, list)
        and hasattr(response.content[0], "text")
    ):
        return response.content[0].text.strip()
    else:
        return "Error summarizing explanations"


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def get_download_button(df, filename, button_text):
    csv = convert_df(df)
    return download_button(csv, filename, button_text)


def main():
    st.title("HiveSight")
    st.write(
        "Ask Claude a binary question multiple times and see the percentage of 'yes' responses."
    )

    model_type = st.selectbox("Choose Model Type", ("Haiku", "Sonnet", "Opus"))
    question = st.text_area("Enter your binary question")
    num_queries = st.number_input(
        "Number of Queries", min_value=1, max_value=100, value=10, step=1
    )
    request_explanation = st.checkbox("Request Explanation")
    use_async = st.checkbox("Use Async")

    if st.button("Ask Claude"):

        progress_bar = st.empty()
        status_text = st.empty()

        if use_async:
            raw_responses = asyncio.run(
                query_claude_async(question, model_type, request_explanation, num_queries)
            )

            valid_responses = [is_valid_response(r_text, request_explanation) for r_text in raw_responses]
            yes_responses = [
                r_text.lower().startswith("yes") and is_valid
                for r_text, is_valid in zip(raw_responses, valid_responses)
            ]
            no_responses = [
                r_text.lower().startswith("no") and is_valid
                for r_text, is_valid in zip(raw_responses, valid_responses)
            ]

            valid_responses = sum(valid_responses)
            yes_count = sum(yes_responses)
            no_count = sum(no_responses)
            explanations = raw_responses if request_explanation else []
        else:
            yes_count = 0
            no_count = 0
            valid_responses = 0
            raw_responses = []
            explanations = []

            for i in range(num_queries):
                response_text = query_claude(
                    question, model_type, request_explanation
                )
                raw_responses.append(response_text)
                if is_valid_response(response_text, request_explanation):
                    if response_text.lower().startswith("yes"):
                        yes_count += 1
                    else:
                        no_count += 1
                    valid_responses += 1
                    if request_explanation:
                        explanations.append(response_text)

                progress = (i + 1) / num_queries
                progress_bar.progress(progress)
                status_text.text(f"Processing query {i+1} of {num_queries}")
                time.sleep(0.1)  # Add a small delay for better visual effect

        if request_explanation and valid_responses > 0:
            status_text.text("Summarizing explanations...")
            explanation_summary = summarize_explanations(explanations)
            status_text.empty()

        progress_bar.empty()

        if valid_responses > 0:
            yes_percentage = yes_count / valid_responses * 100

            # Calculate the 95% confidence interval for the 'yes' probability
            ci_low, ci_high = beta.interval(0.95, yes_count + 1, no_count + 1)
            ci_low *= 100
            ci_high *= 100

            success_text = (
                f"Of {valid_responses} valid responses, Claude said 'yes' {yes_percentage:.1f}% of the time "
                f"(95% CI: [{ci_low:.1f}%, {ci_high:.1f}%])"
            )
            if request_explanation:
                success_text += (
                    "\n\nSummary of Explanations:\n" + explanation_summary
                )

            st.success(success_text)

            # Create a DataFrame from the raw responses
            df = pd.DataFrame({"Response": raw_responses})

            # Create a custom download button for the raw responses
            download_button_str = get_download_button(
                df, "raw_responses.csv", "Download Raw Responses"
            )
            st.markdown(download_button_str, unsafe_allow_html=True)
        else:
            st.error("No valid responses received from Claude.")


if __name__ == "__main__":
    main()
