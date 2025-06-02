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
    st.subheader("**📔Story Telling** - From Rivers to Oceans: Why These States Matter for SDG 14: Life Below Water")
    st.write("This dataset includes data from various states🗽, each contributing to the understanding of aquatic ecosystems and biodiversity. The states involved are crucial for monitoring and preserving marine life, aligning with the Sustainable Development Goal 14: Life Below Water. By analyzing this data, we can gain insights into the health of aquatic environments, species distribution, and the impact of human activities on marine ecosystems. Each of these states plays a surprising role in the health of marine ecosystems:\n")
    st.write("- **West Virgina** and **Kentucky's** coal and gas operations can release harmful chemical to water source such as river.\n")
    st.write("- **Ohio** and **Pennsylvania's** have strong manufacturing and industrial sectors that contribute industrial runoff into waterways\n")
    st.write("- **New Jersey**, **Maryland** and **Virginia** experiencing fast urbanization and these states are coastal states that potentially to send large volume of waste into the ocean.\n")
    st.write("*Assisted by Wikipedia*\n")
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
    st.subheader("**📔Story Telling** - Title: The Ripple Effect: Understanding RBP Scores Across States\n")
    st.write("Pollution doesn’t always start in the ocean—it often begins far inland.")
    st.write("When it rains, chemicals, plastic, and waste from farms, cities, and factories wash into rivers. This is called **River Basin Pollution (RBP)**. The river carries all of it downstream, eventually spilling into the ocean.\n")
    st.write("This dataset shows the average RBP scores for each state in the USA. The scores range from 0 to 100, with higher numbers indicating more pollution. The map highlights states with high RBP scores, showing where pollution is a big problem.\n")
    st.write("In general, states with high RBP scores are often those with large cities, heavy industry, or intensive agriculture. These areas produce a lot of waste that can end up in rivers and oceans.\n")
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
    st.subheader("**📔Story Telling** - Title: The Awakening Tide: A Story of Rising Awareness for Life Below Water\n")
    st.write("At the turn of the 21st century, the world was waking up—not to an alarm clock, but to an ocean in distress. In the past decade, the average abundance of fish species in the United States has shown a significant upward trend, reflecting a growing awareness and commitment to preserving aquatic ecosystems. This increase is particularly notable in states like West Virginia, Kentucky, Ohio, Pennsylvania, New Jersey, Maryland, and Virginia, where conservation efforts have been implemented to protect marine life and habitats. The data suggests that these states are not only crucial for biodiversity but also play a pivotal role in the broader narrative of sustainable development and environmental stewardship. This trend aligns with the Sustainable Development Goal 14: Life Below Water, which emphasizes the importance of conserving and sustainably using the oceans, seas, and marine resources. The rising abundance of fish species serves as a positive indicator of the health of aquatic ecosystems and the effectiveness of conservation initiatives. As we continue to monitor these changes, it is essential to maintain our efforts in protecting marine life and ensuring a sustainable future for our oceans.\n")
    st.write("However, the journey is far from over. The data also reveals that while most states have made significant strides after significant rise of average abundance at the early 21st century, This was possibly due to the fast paced development and urbanization that leads to decline in marine population. The path forward requires a collective effort to address these issues, ensuring that the oceans remain vibrant and resilient for generations to come. As we look to the future, the story of rising fish abundance is not just about numbers; it is about the awakening tide of awareness and action towards a healthier planet.\n")
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
