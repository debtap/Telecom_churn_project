"""Interactive Streamlit dashboard for the synthetic telecom churn dataset."""

from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Telecom Churn Explorer", page_icon="📊", layout="wide")
DATA_PATH = Path(__file__).parent / "telecom_customer_churn.csv"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["total_charges"] = data["total_charges"].fillna(
        data["monthly_charges"] * data["tenure_months"]
    )
    data["online_security"] = data["online_security"].fillna("Not recorded")
    data["tenure_group"] = pd.cut(
        data["tenure_months"],
        bins=[-1, 11, 35, float("inf")],
        labels=["New customer", "Growing customer", "Long-term customer"],
    )
    return data


st.title("Telecom Customer Churn Explorer")
st.caption("Explore churn patterns in a synthetic teaching dataset. These patterns are illustrative, not causal evidence.")

if not DATA_PATH.exists():
    st.error("Dataset not found. Place telecom_customer_churn.csv beside app.py.")
    st.stop()

df = load_data(DATA_PATH)
churned = df["churn"].eq("Yes")
total_customers = df["customer_id"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{total_customers:,}")
col2.metric("Churn rate", f"{churned.mean():.1%}")
col3.metric("Avg. monthly charge", f"${df['monthly_charges'].mean():,.2f}")
col4.metric("Avg. tenure", f"{df['tenure_months'].mean():.1f} months")

st.subheader("Explore the data")
contracts = ["All"] + sorted(df["contract"].dropna().unique().tolist())
selected_contract = st.selectbox("Contract type", contracts)
view = df if selected_contract == "All" else df[df["contract"] == selected_contract]

left, right = st.columns(2)
with left:
    st.markdown("**Churn by contract**")
    contract_rates = pd.crosstab(df["contract"], df["churn"], normalize="index").mul(100)
    st.bar_chart(contract_rates)
with right:
    st.markdown("**Monthly charges by churn status**")
    charge_summary = df.groupby("churn")["monthly_charges"].mean().rename("Average monthly charge")
    st.bar_chart(charge_summary)

st.markdown("**Tenure and monthly charges**")
st.scatter_chart(view, x="tenure_months", y="monthly_charges", color="churn", size="support_tickets")

st.subheader("Customer records")
st.dataframe(
    view[["customer_id", "contract", "tenure_months", "monthly_charges", "support_tickets", "churn", "tenure_group"]],
    use_container_width=True,
    hide_index=True,
)
st.download_button(
    "Download filtered records as CSV",
    data=view.to_csv(index=False).encode("utf-8"),
    file_name="telecom_churn_filtered.csv",
    mime="text/csv",
)

st.info("Data is synthetic and contains 100 teaching records. Use real customer data only after reviewing privacy and access requirements.")
