import plotly as pt
import pandas as pd
import numpy as np
import plotly.express as px

# Load the dataset
df = pd.read_csv('datasets/Combined_Less.csv')

def state_involved():
    """
    This function returns a fig with the states involved in analysis.
    """
    involved_states = df['state'].unique()
    highlight_df = pd.DataFrame({'state': involved_states, 'involved': 1})
    print("States discovered in the dataset:\n", involved_states)

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

    fig.show()


def state_id ():
    """
    This function returns a fig with the the geographical coordinates map of each fish is found.
    """
    fig = px.scatter_mapbox(df,
                            lat="LAT_DD",
                            lon="LON_DD",
                            color="state",
                            hover_name="SITE_ID",
                            zoom=5,
                            height=500)
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()
    return fig

def abundance_location():
    """
    This function returns a fig with the abundance of fish species in different locations.
    """
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
    return fig

def avg_abundance():
    """
    This function returns a fig with the average abundance of fish species in different locations.
    """
    avg_abundance = df.groupby('species')['ABUND'].mean().reset_index()
    fig = px.bar(avg_abundance, x='species', y='ABUND',
                 title='Average Abundance of Fish Species Over Years',
                 labels={'ABUND': 'Average Abundance', 'species': 'Fish Species'})
    fig.update_layout(xaxis_title='Fish Species', yaxis_title='Average Abundance')
    return fig

def avg_abundance_by_species():
    """
    This function returns a fig with the average abundance of fish species in different locations.
    """
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
    return fig

def avg_abundance_by_state():
    """
    This function returns a fig with the average abundance of fish species in different states.
    """
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
    return fig

def seasonal_changes():
    """
    This function returns a fig with the seasonal changes in fish abundance.
    """
    df['month'] = pd.to_datetime(df['DATE']).dt.month
    seasonal_abundance = df.groupby(['month', 'species'])['ABUND'].mean().reset_index()

    fig = px.line(
        seasonal_abundance,
        x='month',
        y='ABUND',
        color='species',
        title='Seasonal Changes in Fish Abundance',
        markers=True
    )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Average Abundance',
        legend_title='Fish Species',
        height=600
    )
    return fig

def rbp_analysis_by_species ():
    """
    This function returns a fig with the RBP analysis of fish species.
    """
    rbp_df = df.groupby('species')['RBP'].mean().reset_index()

    fig = px.bar(
        rbp_df,
        x='species',
        y='RBP',
        title='RBP Analysis of Fish Species',
        labels={'RBP': 'RBP Value', 'species': 'Fish Species'},
        color='RBP',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    fig.update_layout(
        xaxis_title='Fish Species',
        yaxis_title='RBP Value',
        height=600
    )
    return fig

def rbp_analysis_by_state():
    """
    This function returns a fig with the RBP analysis of fish species by state.
    """
    rbp_state_df = df.groupby(['state', 'species'])['RBP'].mean().reset_index()

    fig = px.bar(
        rbp_state_df,
        x='state',
        y='RBP',
        color='species',
        title='RBP Analysis of Fish Species by State',
        labels={'RBP': 'RBP Value', 'state': 'State'},
        barmode='group'
    )

    fig.update_layout(
        xaxis_title='State',
        yaxis_title='RBP Value',
        legend_title='Fish Species',
        height=600
    )
    return fig

def avg_rbp_score_by_state():
    """
    This function returns a fig with the average RBP score by state.
    """
    state_avg = df.groupby('state', as_index=False)['rbpscore'].mean()

    fig = px.choropleth(state_avg,
                        locations='state',
                        locationmode='USA-states',
                        color='rbpscore',
                        color_continuous_scale='Viridis',
                        scope='usa',
                        title='Average RBP Score by State')
    return fig

def abundance_over_years_by_state ():
    """
    This function returns a fig with the average abundance of fish species over the years by state.
    """
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

    return fig
