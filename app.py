
import streamlit as st
import pandas as pd
import pydeck as pdk

# Load processed CSV
df = pd.read_csv("aggregated_parking_by_hour.csv")

st.title("🚗 Melbourne CBD Parking Availability Predictor")

# Sidebar for filtering
selected_date = st.sidebar.selectbox("Select Date", sorted(df['date'].unique()))
selected_hour = st.sidebar.slider("Select Hour (0–23)", 0, 23, 12)

# Filter data
filtered = df[(df['date'] == selected_date) & (df['hour'] == selected_hour)]

# Sort by most empty (lowest occupancy)
recommended = filtered.sort_values(by="occupancy_rate").head(10)
st.subheader(f"Top 10 Recommended Parking Spots at {selected_hour}:00 on {selected_date}")

# Show table
st.dataframe(recommended[['lat', 'lon', 'occupancy_rate']])

# Map visualization
st.map(recommended[['lat', 'lon']])

# Optional: bar chart
st.subheader("Occupancy Rates for Top 10")
st.bar_chart(1 - recommended.set_index(['lat', 'lon'])['occupancy_rate'])

st.caption("Data source: City of Melbourne Open Data")
