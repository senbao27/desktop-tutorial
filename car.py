import pickle
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Melbourne CBD Forecast", page_icon="🚗", layout="centered")

@st.cache_resource
def load_payload(pkl_path: str):
    with open(pkl_path, "rb") as f:
        payload = pickle.load(f)
    model = payload["model"]
    meta = payload.get("metadata", {})
    observed = payload.get("observed", {})
    return model, meta, observed

st.title("Melbourne CBD Forecast")
st.caption("Input year(s) to get observed values (if available) or forecasts from the model.")

# --- Model picker ---
st.sidebar.header("Model")
model_path = st.sidebar.text_input(
    "Path to model .pkl",
    value="melbourne_cbd_population_model.pkl",  # change default if needed
    help="Pickle created by train_and_save.py (must include {'model','metadata','observed'})."
)
uploaded = st.sidebar.file_uploader("Or upload a .pkl", type=["pkl"])

if uploaded is not None:
    # Load from uploaded file in memory
    payload = pickle.load(uploaded)
    model = payload["model"]
    meta = payload.get("metadata", {})
    observed = payload.get("observed", {})
else:
    # Load from disk path
    try:
        model, meta, observed = load_payload(model_path)
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.stop()

# --- Input years ---
years_text = st.text_input(
    "Enter year(s) separated by commas",
    value="2016, 2021, 2026, 2030"
)
try:
    years = [int(x.strip()) for x in years_text.split(",") if x.strip() != ""]
except Exception:
    st.error("Please enter valid integers separated by commas.")
    st.stop()

# --- Predict ---
def predict_year(y: int):
    if int(y) in observed:
        return float(observed[int(y)]), "observed"
    yhat = float(model.predict(np.array([[y]], dtype=float))[0])
    tag = "forecast"
    ymin, ymax = meta.get("train_year_min"), meta.get("train_year_max")
    if ymin is not None and ymax is not None and ymin <= y <= ymax:
        tag = "fit"
    return yhat, tag

rows = []
for y in years:
    val, typ = predict_year(y)
    rows.append({"Year": y, "Value": val, "Type": typ})

df = pd.DataFrame(rows).sort_values("Year").reset_index(drop=True)

st.subheader("Results")
st.dataframe(df, use_container_width=True)

# Simple chart
st.subheader("Trend")
st.line_chart(df.set_index("Year")["Value"])

# Meta
with st.expander("Model metadata"):
    st.json(meta)
