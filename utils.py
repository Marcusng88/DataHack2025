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