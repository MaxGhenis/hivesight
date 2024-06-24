from policyengine_us import Microsimulation
import pandas as pd

sim = Microsimulation(dataset="enhanced_cps_2022")


def get(var):
    return sim.calc(var, period=2024, map_to="person")


age = get("age")
state = get("state_code")
income = get("employment_income")

df = pd.DataFrame(
    {"age": age, "state": state, "income": income, "weight": age.weights}
)

# Aggregate by all variables except weight.
df_dedup = df.groupby(["age", "state", "income"]).weight.sum().reset_index()

df_dedup.to_csv("perspectives.csv", index=False)
