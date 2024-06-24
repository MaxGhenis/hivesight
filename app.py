import streamlit as st
from visualization import create_enhanced_visualizations
from analysis import analyze_responses, create_pivot_table
from simulation import batch_simulate_responses
from custom_components import download_button
from config import MODEL_MAP

import pandas as pd


def main():
    st.title("🐝 HiveSight")
    st.write("Ask AIs anything.")

    question_ls = st.text_area(
        "Enter your statement in a form to agree or disagree with.",
        key="question_ls",
    )

    num_queries = st.number_input(
        "Number of Responses",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
    )

    with st.expander("Additional Options", expanded=False):
        model_type = st.selectbox(
            "Choose Model Type",
            list(MODEL_MAP.keys()),
        )
        st.write("Demographic Filters (optional)")
        age_range = st.slider("Age Range", 0, 100, (18, 100))
        income_range = st.slider(
            "Income Range ($)", 0, 1_000_000, (0, 1_000_000)
        )

    groupby_var = st.selectbox("Group By", ["age", "income"], index=0)

    if st.button("Run Simulation"):
        statement = question_ls

        with st.spinner("Simulating responses..."):
            responses = batch_simulate_responses(
                statement,
                None,  # No choices for Likert scale
                num_queries,
                model_type,
                age_range,
                income_range,
                "likert",  # Passing "likert" as a fixed parameter
            )

            if not responses:
                st.error(
                    "No valid responses were generated. Please try again or adjust your parameters."
                )
                return

            response_counts = analyze_responses(responses)
            pivot_table = create_pivot_table(
                pd.DataFrame(responses), groupby_var
            )
            visualizations = create_enhanced_visualizations(
                response_counts, pivot_table, groupby_var
            )

        st.success(
            f"Simulation complete. Generated {len(responses)} valid responses."
        )

        st.subheader("Analysis")
        st.write(f"Mean Score: {response_counts['percentage'].mean():.2f}")
        st.write(f"Median Score: {response_counts['percentage'].median():.2f}")
        st.write(
            f"Standard Deviation: {response_counts['percentage'].std():.2f}"
        )
        st.write(f"Total Responses: {response_counts['percentage'].sum()}")

        ci_low, ci_high = response_counts["percentage"].quantile(
            [0.025, 0.975]
        )
        if ci_low is not None and ci_high is not None:
            st.write(f"95% Confidence Interval: [{ci_low:.2f}, {ci_high:.2f}]")
        else:
            st.write("95% Confidence Interval: Not available")

        st.subheader("Visualizations")
        for fig in visualizations:
            st.plotly_chart(fig)

        df = pd.DataFrame(responses)
        download_button_str = download_button(
            df, "simulated_responses.csv", "Download Simulated Responses"
        )
        st.markdown(download_button_str, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
