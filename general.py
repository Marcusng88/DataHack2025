import plotly as pt
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


def state_involved(df):
    st.write("**1. State Involved in This Reasearch**")
    involved_states = df['state'].unique()
    highlight_df = pd.DataFrame({'state': involved_states, 'involved': 1})

    fig = px.choropleth(
        highlight_df,
        locations='state',
        locationmode='USA-states',
        color='involved',
        color_continuous_scale=[[0, 'lightgray'], [1, 'blue']],
        scope='usa',
        title='States Involved in the Dataset'
    )

    fig.update_layout(
        coloraxis_showscale=False,  # Hide colorbar
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


def state_id (df):
    st.write("**2. Appearance Location of Each Species**")
    fig = px.scatter_mapbox(df,
                            lat="LAT_DD",
                            lon="LON_DD",
                            color="state",
                            hover_name="SITE_ID",
                            zoom=5,
                            height=500)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def abundance_location(df):
    st.write("**3. Species Abundance by Location**")
    fig = px.scatter_mapbox(df,
                            lat="LAT_DD",
                            lon="LON_DD",
                            color="species",
                            hover_name="SITE_ID",
                            hover_data={"species": True, "ABUND": True, "LAT_DD": False, "LON_DD": False},
                            zoom=5,
                            height=500,
                            title='Species Abundance by Location')
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def avg_abundance(df):
    st.write("**4. Average Abundance of Fish Species Over Years**")
    avg_abundance = df.groupby('species')['ABUND'].mean().reset_index()
    fig = px.bar(avg_abundance, x='species', y='ABUND',
                 title='Average Abundance of Fish Species Over Years',
                 labels={'ABUND': 'Average Abundance', 'species': 'Fish Species'})
    fig.update_layout(xaxis_title='Fish Species', yaxis_title='Average Abundance')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def avg_abundance_by_species(df):
    st.write("**5. Average Abundance Over Years by Species**")
    avg_abundance_by_year = df.groupby(['species', 'YEAR'])['ABUND'].mean().reset_index()

    species_year_counts = avg_abundance_by_year['species'].value_counts()
    valid_species = species_year_counts[species_year_counts >= 2].index
    filtered_data = avg_abundance_by_year[avg_abundance_by_year['species'].isin(valid_species)]

    fig = px.line(
        filtered_data,
        x="YEAR",
        y="ABUND",
        color="species",
        title="Average Abundance Over Years by Species",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Abundance",
        legend_title="Species",
        hovermode="x unified",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def avg_abundance_by_state(df):
    st.write("**6. Average Abundance of Fish Species Over Years by State**")
    avg_abundance_by_state = df.groupby(['state', 'species'])['ABUND'].mean().reset_index()

    fig = px.bar(
        avg_abundance_by_state,
        x='state',
        y='ABUND',
        color='species',
        title='Average Abundance of Fish Species by State',
        labels={'ABUND': 'Average Abundance', 'state': 'State'},
        barmode='group'
    )

    fig.update_layout(
        xaxis_title='State',
        yaxis_title='Average Abundance',
        legend_title='Fish Species',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def seasonal_changes(df):
    st.write("**7. Seasonal Changes in Fish Abundance**")
    fig = px.box(df, x='month', y='Temp', title='Temperature by Month',color='month')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def rbp_analysis_by_species (df):
    st.write("**8. RBP Analysis of Fish Species**")
    rbp_df = df.groupby('species')['rbpscore'].mean().reset_index()

    fig = px.bar(
        rbp_df,
        x='species',
        y='rbpscore',
        title='RBP Analysis of Fish Species',
        labels={'rbpscore': 'RBP Value', 'species': 'Fish Species'},
        color='rbpscore',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    fig.update_layout(
        xaxis_title='Fish Species',
        yaxis_title='RBP Value',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def rbp_analysis_by_state(df):
    st.write("**9. RBP Analysis of Fish Species by State**")
    rbp_state_df = df.groupby(['state', 'species'])['rbpscore'].mean().reset_index()

    fig = px.bar(
        rbp_state_df,
        x='state',
        y='rbpscore',
        color='species',
        title='RBP Analysis of Fish Species by State',
        labels={'rbpscore': 'RBP Value', 'state': 'State'},
        barmode='group'
    )

    fig.update_layout(
        xaxis_title='State',
        yaxis_title='RBP Value',
        legend_title='Fish Species',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def avg_rbp_score_by_state(df):
    st.write("**10. Average RBP Score by State**")
    state_avg = df.groupby('state', as_index=False)['rbpscore'].mean()

    fig = px.choropleth(state_avg,
                        locations='state',
                        locationmode='USA-states',
                        color='rbpscore',
                        color_continuous_scale='Viridis',
                        scope='usa',
                        title='Average RBP Score by State')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def abundance_over_years_by_state (df):
    st.write("**11. Average Abundance Over Years by State**")
    sum_by_state = df.groupby(['state','YEAR'])['TotCount'].sum().reset_index()
    fig = px.line(
        sum_by_state,
        x="YEAR",
        y="TotCount",
        color="state",
        title="Average Abundance Over Years by State",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Abundance",
        legend_title="State",
        hovermode="x unified",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def general_eda(df):
    st.write("This section provides an overview of the dataset and general trends.")

    # 1. State Involved
    state_involved(df)

    # 2. Appearance Location of Each Species
    state_id(df)

    # 3. Species Abundance by Location
    abundance_location(df)

    # 4. Average Abundance of Fish Species Over Years
    avg_abundance(df)

    # 5. Average Abundance Over Years by Species
    avg_abundance_by_species(df)

    # 6. Average Abundance of Fish Species Over Years by State
    avg_abundance_by_state(df)

    # 7. Seasonal Changes in Fish Abundance
    seasonal_changes(df)

    # 8. RBP Analysis of Fish Species
    rbp_analysis_by_species(df)

    # 9. RBP Analysis of Fish Species by State
    rbp_analysis_by_state(df)

    # 10. Average RBP Score by State
    avg_rbp_score_by_state(df)

    # 11. Average Abundance Over Years by State
    abundance_over_years_by_state(df)
