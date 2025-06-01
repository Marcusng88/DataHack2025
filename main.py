import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from .specific_case import species_specific_eda

# -----------------------------------------------------
# 1. LOAD / PREPARE YOUR DATA
# -----------------------------------------------------
@st.cache_data
def load_data():
    # Replace this with your actual data-loading logic.
    # For example: pd.read_csv("your_file.csv")
    # Here we simulate with random data—swap in your real df.
    n = 1000
    rng = np.random.default_rng(42)
    df = pd.read_csv('datasets\Combined_Less.csv')
    return df

df = load_data()

st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose View", ["General EDA", "Species Search"])

# -----------------------------------------------------
# 4. GENERAL EDA SECTION
# -----------------------------------------------------
if mode == "General EDA":
    st.header("🗺️ Global Exploratory Analysis")
    st.write("Coming soon or add your general EDA here...")

# -----------------------------------------------------
# 5. SPECIES-LEVEL SEARCH SECTION
# -----------------------------------------------------
elif mode == "Species Search":
    species_specific_eda(df)
    


# -----------------------------------------------------
# 5. OPTIONAL FOOTER / NOTES
# -----------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(
    "⚙️ Data Source: Replace `load_data()` with your CSV/DB.\n\n"
    "🔎 Species Search is case-insensitive and will match substrings.\n\n"
    "📊 All EDA plots are generated with Plotly for interactivity."
)