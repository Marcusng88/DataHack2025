import streamlit as st

def get_API():
    GOOGLE_API_KEY = st.text_input(
        "Google API Key",
        type="password",
        help="Enter your Google API key here. This is required for accessing Google services."
    )
    if not GOOGLE_API_KEY:
        st.warning("Please enter your Google API key to proceed.")
    return GOOGLE_API_KEY

def get_Tavily_API():
    TAVILY_API_KEY = st.text_input(
        "Tavily API Key",
        type="password",
        help="Enter your Tavily API key here. This is required for accessing Tavily services."
    )
    if not TAVILY_API_KEY:
        st.warning("Please enter your Tavily API key to proceed.")  
    return TAVILY_API_KEY