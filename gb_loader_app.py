
import streamlit as st, joblib, pandas as pd, numpy as np
from datetime import datetime, timedelta

@st.cache_resource
def load_model():
    return joblib.load("gb_model.pkl")

model = load_model()

def reno_factor(scope):
    s = scope.upper()
    if "NEW" in s and "RENO" in s: return 1.15
    if "EXP" in s and "RENO" in s: return 1.20
    if "RENO" in s: return 1.30
    return 1.0

st.title("📐 BIM Duration Estimator (GB Model)")

start = st.date_input("Start Date", value=datetime.today())
scope = st.selectbox("Scope", ["NEW","RENO","EXP","B.O."])
contract = st.selectbox("Contract", ["BB","DA","AB"])
btype = st.selectbox("Building Type", ["Civic/Specialty","Commercial","Education","Healthcare","Hospitality/Residential","Industrial","Mission Critical"])
sqft = st.number_input("Square Footage", min_value=1000, value=50000)
levels = st.number_input("Levels", min_value=1, value=1)

if st.button("Predict"):
    logsf = np.log(sqft)
    reno = reno_factor(scope)
    X = pd.DataFrame([{
        "LogSqFt": logsf,
        "Levels": levels,
        "Levels_LogSqFt": levels*logsf,
        "RenovationFactor": reno,
        "Renov_LogSqFt": reno*logsf,
        "Renov_Levels": reno*levels,
        "Scope": scope,
        "Contract": contract,
        "Building Type": btype
    }])
    dur = model.predict(X)[0]
    end = start + timedelta(days=int(round(dur)))
    st.success(f"Predicted Duration: {dur:.1f} days")
    st.info(f"Predicted End Date: {end:%Y-%m-%d}")
