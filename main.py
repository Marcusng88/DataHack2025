import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from specific_case import species_specific_eda


@st.cache_data
def load_data():
    df = pd.read_csv('datasets\Combined_Less.csv')
    return df

df = load_data()

st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose View", ["General EDA", "Species Search"])


if mode == "General EDA":
    st.header("🗺️ Global Exploratory Analysis")
    st.write("Coming soon or add your general EDA here...")


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
