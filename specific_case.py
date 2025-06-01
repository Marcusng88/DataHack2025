import streamlit as st
import plotly.express as px

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

    # Map common names to species
    species_mapping = df[["Common_Name", "species"]].dropna().drop_duplicates()
    name_to_species = dict(zip(species_mapping["Common_Name"], species_mapping["species"]))

    # Sidebar dropdown
    common_name_input = st.sidebar.selectbox("Select species (by common name):", list(name_to_species.keys()))
    species_input = name_to_species[common_name_input]

    # Filter
    df_spec = df[df["species"] == species_input]

    st.subheader(f"Showing EDA for '{common_name_input}' ({species_input})")

    abundance_trend_over_years(df_spec, common_name_input)
    abundance_by_state(df_spec, common_name_input)
    map_of_locations(df_spec, common_name_input)
    nitrogen_vs_abundance(df_spec, common_name_input)
    summary_statistics(df_spec)