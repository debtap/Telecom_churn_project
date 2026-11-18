# Telecom Customer Churn Explorer

An interactive Streamlit dashboard for exploring a synthetic telecom customer churn dataset. It shows headline churn metrics, contract comparisons, charge patterns, tenure relationships, and customer records.

## Dataset

`telecom_customer_churn.csv` contains 100 synthetic teaching records. It does not contain real customer information. Patterns are illustrative and should not be interpreted as proof of causation.

## Run locally

1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies and start the app:

   ```powershell
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```

The original command-line analysis is also available with `python telecom_churn_analysis.py`.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Choose **Create app**, select this repository and branch, and set the main file path to `app.py`.
4. Deploy. Streamlit installs packages from `requirements.txt`.

Keep the CSV in the repository for this synthetic sample app. Do not commit real or confidential customer data.
