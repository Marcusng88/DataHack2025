import streamlit as st
import plotly.express as px
from tavily import TavilyClient
from utils import get_Tavily_API
from adk_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

import plotly.io as pio
import asyncio

def info_image (species_input):
    tavily_client = TavilyClient(api_key=get_Tavily_API())

    st.header(f"🌄 Image Search and Basic Information for '{species_input}'")

    tavily_tool = TavilyToolSpec(api_key=TAVILY_API_KEY)


session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()
APP_NAME = "datahacks2025"
USER_ID = "user_1"
SESSION_ID = "session_001"
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service,artifact_service=artifact_service)
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME, 
    user_id=USER_ID, 
    session_id=SESSION_ID
))
async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found


async def call_agent_for_existed_graph_insight(query, runner, user_id, session_id):
    query = pio.to_json(query)
    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found
    print(final_response_text)
    return final_response_text



def abundance_trend_over_years(df_spec, species_input):
    st.write("**1. Abundance Trend Over Years**")
    avg_abund_spec = df_spec.groupby("YEAR")["ABUND"].mean().reset_index()
    fig = px.line(
        avg_abund_spec,
        x="YEAR",
        y="ABUND",
        title=f"Average Abundance of '{species_input}' Over Years",
        markers=True,
        height=400,
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Avg Abundance")
    response = asyncio.run(call_agent_for_existed_graph_insight(fig,runner,user_id=USER_ID,session_id=SESSION_ID))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(response)
    st.markdown("---")

def abundance_by_state(df_spec, species_input):
    st.write("**2. Abundance by State**")
    avg_abund_state_spec = df_spec.groupby(["state", "YEAR"])["ABUND"].mean().reset_index()
    fig = px.line(
        avg_abund_state_spec,
        x="YEAR",
        y="ABUND",
        color="state",
        title=f"Average Abundance of '{species_input}' by State Over Years",
        markers=True,
        height=400,
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Avg Abundance")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def map_of_locations(df_spec, species_input):
    st.write("**3. Map of Locations**")
    df_map_spec = df_spec[df_spec["ABUND"] > 0].copy()
    fig = px.scatter_mapbox(
        df_map_spec,
        lat="LAT_DD",
        lon="LON_DD",
        size="ABUND",
        color="state",
        hover_name="SITE_ID",
        hover_data={"ABUND": True, "YEAR": True},
        zoom=4,
        height=500,
        title=f"Locations & Abundance of '{species_input}'",
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def nitrogen_vs_abundance(df_spec, species_input):
    st.write("**4. Nitrogen (TN) vs Abundance for Selected Species**")
    if "TN" in df_spec.columns and df_spec["NO3"].notna().any():
        df_spec_tn = df_spec[df_spec["NO3"].notna() & df_spec["ABUND"].notna()]
        fig = px.scatter(
            df_spec_tn,
            x="NO3",
            y="ABUND",
            trendline="ols",
            title=f"Abundance vs Total Nitrogen for '{species_input}'",
            labels={"NO3": "Total Nitrogen", "ABUND": "Abundance"},
            height=400,
        )
        fig.update_layout(hovermode="closest")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No TN data available for this species.")
    st.markdown("---")

def summary_statistics(df_spec):
    st.write("**5. Summary Statistics**")
    cols = ["ABUND", "TotCount", "rbpscore", "TN", "PHSTVL", "COND"]
    available_cols = [col for col in cols if col in df_spec.columns]
    st.write(df_spec[available_cols].describe())

def species_specific_eda(df):
    st.header("🔍 Species-Specific EDA")

    # Mapping
    species_mapping = df[["Common_Name", "species"]].dropna().drop_duplicates()
    name_to_species = dict(zip(species_mapping["Common_Name"], species_mapping["species"]))

    # Sidebar toggle: dropdown or search
    input_mode = st.sidebar.radio("Select species by:", ["Dropdown", "Search"])

    if input_mode == "Dropdown":
        common_name_input = st.sidebar.selectbox("Choose Common Name:", list(name_to_species.keys()))
        species_input = name_to_species[common_name_input]

    else:  # Search
        user_input = st.sidebar.text_input("Type species name (common or scientific):", "")
        matched_rows = df[
            df["Common_Name"].str.contains(user_input, case=False, na=False) |
            df["species"].str.contains(user_input, case=False, na=False)
        ]
        

        if user_input:
            image_link =  asyncio.run(call_agent_for_image(query=user_input,runner=runner,user_id=USER_ID,session_id=SESSION_ID))
            if image_link != 'not_found':
                try:
                    st.image(image_link)
                except:
                    return
        if matched_rows.empty:
            st.warning("No species match your input.")
            return
        common_name_input = matched_rows["Common_Name"].iloc[0]
        species_input = matched_rows["species"].iloc[0]

    df_spec = df[df["species"] == species_input]
    
    st.subheader(f"Showing EDA for '{common_name_input}' ({species_input})")

    # Call each modular plot
    info_image(species_input)
    abundance_trend_over_years(df_spec, species_input)
    abundance_by_state(df_spec, species_input)
    map_of_locations(df_spec, species_input)
    nitrogen_vs_abundance(df_spec, species_input)

    abundance_trend_over_years(df_spec, common_name_input)
    abundance_by_state(df_spec, common_name_input)
    map_of_locations(df_spec, common_name_input)
    nitrogen_vs_abundance(df_spec, common_name_input)
    summary_statistics(df_spec)