import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon
st.set_page_config(
    page_title='Top 50 busiest airports',
    page_icon='airport.png',
)

# Load data from CSV
@st.cache_data
def get_total_data():
    DATA_FILENAME = Path(__file__).parent/'data/airport_data_2017_2023.csv'
    total_df = pd.read_csv(DATA_FILENAME)

    # Convert 'Year' to numeric type if needed
    total_df['Year'] = pd.to_numeric(total_df['Year'])
    return total_df

total_df = get_total_data()

# Draw the page title
st.title("🛫 Top 50 busiest airports")

# Select year range
min_value = total_df['Year'].min()
max_value = total_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=int(min_value),
    max_value=int(max_value),
    value=[int(min_value), int(max_value)]
)

# Select countries
countries = total_df['Country'].unique()
selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['Vietnam', 'United States', 'United Kingdom', 'United Arab Emirates', 'Turkey', 'Thailand', 'Spain', 'South Korea', 'Singapore', 'Saudi Arabia', 'Qatar', 'Philippines', 'Netherlands', 'Mexico', 'Malaysia', 'Japan', 'Indonesia', 'India', 'Germany', 'France', 'China', 'Canada', 'Brazil']
)

# Filter the data
filtered_total_df = total_df[
    (total_df['Country'].isin(selected_countries)) &
    (total_df['Year'] >= from_year) &
    (total_df['Year'] <= to_year)
]

# Group data by Country and Year to sum passengers
country_year_total_df = filtered_total_df.groupby(['Country', 'Year'])['Total_passengers'].sum().reset_index()

# Display line chart with total passengers by country
st.header('Passenger Traffic by Country over Time')
st.line_chart(
    country_year_total_df,
    x='Year',
    y='Total_passengers',
    color='Country'
)

# Metric for country comparison
st.header(f'Passenger Count Comparison in {to_year}')
cols = st.columns(4)
for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]
    with col:
        first_total = country_year_total_df[(country_year_total_df['Country'] == country) & (country_year_total_df['Year'] == from_year)]['Total_passengers'].sum() / 1e6
        last_total = country_year_total_df[(country_year_total_df['Country'] == country) & (country_year_total_df['Year'] == to_year)]['Total_passengers'].sum() / 1e6
        
        if math.isnan(first_total) or first_total == 0:
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_total / first_total:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} Passengers',
            value=f'{last_total:,.0f}M',
            delta=growth,
            delta_color=delta_color
        )
