

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Load cleaned dataset
df = pd.read_csv("cleaned_parking_data.csv")

# Set Streamlit page settings
st.set_page_config(page_title="Melbourne CBD Parking Predictor", layout="wide")
st.title("Melbourne CBD Parking Predictor")
st.markdown("Select a weekday and hour to explore potential available parking spaces in Melbourne CBD.")

# Sidebar inputs
weekday = st.selectbox("Select weekday", df["day_of_week"].unique())
hour = st.selectbox("Select hour (24-hour format)", sorted(df["hour"].unique()))

# Filter dataset
filtered = df[(df["day_of_week"] == weekday) & (df["hour"] == hour)]

# Sort by availability (1 = available, 0 = occupied)
filtered = filtered.sort_values("unoccupied_rate", ascending=False)

# Create folium map
m = folium.Map(location=[-37.8136, 144.9631], zoom_start=15)

for _, row in filtered.iterrows():
    color = "green" if row["unoccupied_rate"] == 1 else "red"
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["street_name"],
        icon=folium.Icon(color=color)
    ).add_to(m)

# Display map in Streamlit
st_folium(m, width=1000, height=600)

