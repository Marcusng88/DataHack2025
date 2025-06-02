import streamlit as st
import plotly.express as px
from tavily import TavilyClient
import os
from utils import get_Tavily_API
from adk_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

import plotly.io as pio
import asyncio

def info_image_species (species_input):

    api_key = os.getenv('TAVILY_API_KEY')

    if not api_key:
        st.warning("Please provide your Tavily API key to continue.")
        st.stop() 

    try:
        tavily_client = TavilyClient(api_key=api_key)

        st.header(f"🌄 Image Search and Basic Information for '{species_input}'")

        res= tavily_client.search(query=f'description for species {species_input}',include_images=True,max_results=1)
        st.image(res['images'][0])
        if res and "results" in res and len(res["results"]) > 0:
            description = res["results"][0].get("content", "No description available.")
        else:
            description = "No results found."
        st.write(description)
    except:
        return
    


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

    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." 


    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: 
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break
    final_response_text = final_response_text.replace("```markdown", "").replace("```", "").strip()
    return final_response_text


async def call_agent_for_existed_graph_insight(query, runner, user_id, session_id):
    query = pio.to_json(query)
    content = types.Content(role='user', parts=[types.Part(text=query)])

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: 
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break 
    final_response_text = final_response_text.replace("```markdown", "").replace("```", "").strip()
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
    
    st.plotly_chart(fig, use_container_width=True)
    try:
        response = asyncio.run(call_agent_for_existed_graph_insight(fig,runner,user_id=USER_ID,session_id=SESSION_ID))
        st.markdown(response)
    except:
        return
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
    try:
        response = asyncio.run(call_agent_for_existed_graph_insight(fig,runner,user_id=USER_ID,session_id=SESSION_ID))
        st.markdown(response)
    except:
        return
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


def summary_statistics(df_spec):
    st.write("**5. Summary Statistics**")
    cols = ["ABUND", "TotCount", "rbpscore", "TN", "PHSTVL", "COND"]
    available_cols = [col for col in cols if col in df_spec.columns]
    st.write(df_spec[available_cols].describe())

def final_conclusion(species):
    try:
        response = asyncio.run(call_agent_async(species,runner,user_id=USER_ID,session_id=SESSION_ID))
        print(response)
        st.write('Final Conclusion and Insight')
        st.markdown(response)
    except:
        st.markdown('---')
    

def species_specific_eda(df):
    st.header("🔍 Species-Specific EDA")

    # Mapping
    species_mapping = df[["Common_Name", "species"]].dropna().drop_duplicates()
    name_to_species = dict(zip(species_mapping["Common_Name"], species_mapping["species"]))

    # Sidebar toggle: dropdown or search
    input_mode = st.sidebar.radio("Select species by:", ["Dropdown", "Search"])
    user_input = None

    if input_mode == "Dropdown":
        common_name_input = st.sidebar.selectbox("Choose Common Name:", list(name_to_species.keys()))
        species_input = name_to_species[common_name_input]
        user_input = common_name_input

    else:  # Search
        user_input = st.sidebar.text_input("Type species name (common or scientific):", "")
        matched_rows = df[
            df["Common_Name"].str.contains(user_input, case=False, na=False) |
            df["species"].str.contains(user_input, case=False, na=False)
        ]
        
        if matched_rows.empty:
            st.warning("No species match your input.")
            return
        common_name_input = matched_rows["Common_Name"].iloc[0]
        species_input = matched_rows["species"].iloc[0]

    df_spec = df[df["species"] == species_input]
    
    st.subheader(f"Showing EDA for '{common_name_input}' ({species_input})")

    # Call each modular plot
    info_image_species(species_input)
    abundance_trend_over_years(df_spec, species_input)
    abundance_by_state(df_spec, species_input)
    map_of_locations(df_spec, species_input)
    summary_statistics(df_spec)
    final_conclusion(species_input)