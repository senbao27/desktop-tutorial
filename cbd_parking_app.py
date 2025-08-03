
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 加载数据
df = pd.read_csv("cbd_parking_availability_by_time.csv")

# Streamlit 界面标题
st.title("墨尔本CBD车位预测")
st.markdown("选择星期几和时间，查看哪些街道更可能有空车位。")

# 用户选择
weekday = st.selectbox("选择星期几", sorted(df['weekday'].unique()))
hour = st.selectbox("选择时间（24小时制）", sorted(df['hour'].unique()))

# 过滤数据
filtered = df[(df['weekday'] == weekday) & (df['hour'] == hour)]

# 平均占用率从低到高排序（更低=更可能空）
filtered = filtered.sort_values("occupancy_rate")

# 初始化地图
m = folium.Map(location=[-37.8136, 144.9631], zoom_start=15)

# 添加标记
for _, row in filtered.iterrows():
    color = "green" if row['occupancy_rate'] < 0.3 else "orange" if row['occupancy_rate'] < 0.7 else "red"
    popup = f"{row['street_name']}<br>预计空闲率: {1 - row['occupancy_rate']:.0%}"
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        popup=popup,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 显示地图
st_folium(m, width=700, height=500)
