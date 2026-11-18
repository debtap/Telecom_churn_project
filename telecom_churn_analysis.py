# TELECOM CUSTOMER CHURN - PYTHON MINI PROJECT
# Libraries: NumPy, Pandas, Matplotlib, Seaborn
# Scope: No loops, no if-statements, no user-defined functions.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and inspect the customer data (Pandas)
df = pd.read_csv("telecom_customer_churn.csv")
print(df.head())
print(df.shape)
print(df.info())

# 2. NumPy summary calculations on monthly charges
charges = df["monthly_charges"].to_numpy()
print("Average monthly charge:", np.mean(charges))
print("Highest monthly charge:", np.max(charges))
print("Lowest monthly charge:", np.min(charges))
print("Charge spread:", np.ptp(charges))

# 3. Create customer tenure groups using np.select
df["tenure_group"] = np.select(
    [df["tenure_months"] < 12, df["tenure_months"] < 36],
    ["New customer", "Growing customer"],
    default="Long-term customer"
)
print(df[["customer_id", "tenure_months", "tenure_group"]].head(10))

# 4. Identify and handle missing values
print(df.isna().sum())
df["total_charges"] = df["total_charges"].fillna(
    df["monthly_charges"] * df["tenure_months"]
)
df["online_security"] = df["online_security"].fillna("Not recorded")

# 5. Calculate customer lifetime value proxy and average revenue per customer
df["estimated_revenue"] = df["monthly_charges"] * df["tenure_months"]
print(df[["customer_id", "estimated_revenue"]].sort_values(
    "estimated_revenue", ascending=False
).head(10))

# 6. Filter customers who churned
churned_customers = df[df["churn"] == "Yes"]
print(churned_customers[["customer_id", "contract", "tenure_months", "monthly_charges"]])

# 7. Compare churned and retained customers
churn_summary = df.groupby("churn").agg(
    customers=("customer_id", "count"),
    avg_tenure=("tenure_months", "mean"),
    avg_monthly_charge=("monthly_charges", "mean"),
    avg_support_tickets=("support_tickets", "mean")
).round(2)
print(churn_summary)

# 8. Churn rate by contract type
contract_churn = pd.crosstab(
    df["contract"], df["churn"], normalize="index"
).mul(100).round(1)
print(contract_churn)

# 9. Churn rate by payment method
payment_churn = pd.crosstab(
    df["payment_method"], df["churn"], normalize="index"
).mul(100).round(1)
print(payment_churn)

# 10. Customer risk flag using np.where
df["risk_flag"] = np.where(
    (df["contract"] == "Month-to-month") &
    (df["tenure_months"] < 12) &
    (df["support_tickets"] >= 2),
    "High attention", "Regular monitoring"
)
print(df[["customer_id", "contract", "tenure_months", "support_tickets", "risk_flag"]].head(15))

# 11. NumPy percentile analysis of monthly charges
print("25th percentile:", np.percentile(charges, 25))
print("Median:", np.percentile(charges, 50))
print("75th percentile:", np.percentile(charges, 75))

# 12. Matplotlib bar chart: customer count by contract
contract_counts = df["contract"].value_counts()
contract_counts.plot(kind="bar", title="Customers by Contract Type")
plt.xlabel("Contract type")
plt.ylabel("Number of customers")
plt.tight_layout()
plt.show()

# 13. Matplotlib bar chart: churn count
df["churn"].value_counts().plot(kind="bar", title="Churned vs Retained Customers")
plt.xlabel("Customer status")
plt.ylabel("Number of customers")
plt.tight_layout()
plt.show()

# 14. Matplotlib histogram: monthly charges distribution
plt.hist(df["monthly_charges"], bins=12)
plt.title("Distribution of Monthly Charges")
plt.xlabel("Monthly charges")
plt.ylabel("Number of customers")
plt.tight_layout()
plt.show()

# 15. Seaborn boxplot: monthly charges by churn status
sns.boxplot(data=df, x="churn", y="monthly_charges")
plt.title("Monthly Charges: Churned vs Retained")
plt.tight_layout()
plt.show()

# 16. Seaborn countplot: churn by contract
sns.countplot(data=df, x="contract", hue="churn")
plt.title("Churn by Contract Type")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# 17. Seaborn scatterplot: tenure vs monthly charges
sns.scatterplot(data=df, x="tenure_months", y="monthly_charges", hue="churn")
plt.title("Tenure vs Monthly Charges")
plt.tight_layout()
plt.show()

# 18. Seaborn heatmap: correlation between numeric variables
numeric_df = df[[
    "tenure_months", "monthly_charges", "total_charges",
    "support_tickets", "late_payments", "senior_citizen"
]]
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Customer Data Correlation Heatmap")
plt.tight_layout()
plt.show()

# 19. Compare average tenure by churn status
tenure_comparison = df.groupby("churn")["tenure_months"].mean().round(1)
print("Average tenure by churn status:")
print(tenure_comparison)

# 20. Final business summary
print("Total customers:", df["customer_id"].nunique())
print("Churned customers:", (df["churn"] == "Yes").sum())
print("Overall churn rate (%):", round((df["churn"] == "Yes").mean() * 100, 2))
print("Average monthly charge:", round(df["monthly_charges"].mean(), 2))
print("Average tenure (months):", round(df["tenure_months"].mean(), 1))
