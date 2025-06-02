import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from general import general_eda
from specific_case import species_specific_eda
from llamaIndex_agent import agent_interface

# -----------------------------------------------------
# 1. LOAD / PREPARE YOUR DATA
# -----------------------------------------------------
from specific_case import species_specific_eda
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

@st.cache_data
def load_data():
    df = pd.read_csv('datasets\Combined_Less.csv')
    return df

df = load_data()

st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose View", ["🌏General EDA", "🦈Species Search", "🤖LlamaIndex AI agent EDA"])


if mode == "🌏General EDA":
    st.header("🗺️ Global Exploratory Analysis")
    general_eda(df)

elif mode == "🦈Species Search":
    species_specific_eda(df)
    
elif mode == "🤖LlamaIndex AI agent EDA":
    st.header("🧠 Ask our LLM Agent anything about your data!") 
    agent_interface()


st.sidebar.markdown("---")
st.sidebar.markdown(
    "⚙️ Data Source: Replace `load_data()` with your CSV/DB.\n\n"
    "🔎 Species Search is case-insensitive and will match substrings.\n\n"
    "📊 All EDA plots are generated with Plotly for interactivity.\n\n"
    "📈 Refers full Data Science cycle in the [Github Link](https://github.com/Marcusng88/DataHack2025/blob/79e67ba812ec6e840f62ad06a7f91bed2d06aa9f/Hokkien_Mee_is_Black_DataHacks_2025.ipynb)\n\n"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "👨‍💻 Developed by [(Marcus) Ng Zheng Jie](https://www.linkedin.com/in/ng-zheng-jie/) & [(Harry) Cheng Kai Huang](https://www.linkedin.com/in/cheng-kai-huang-913240201/)\n\n"
    "(c) Copyright of Hokkien Mee is Red. All rights reserved. For DataHacks purpose."
)