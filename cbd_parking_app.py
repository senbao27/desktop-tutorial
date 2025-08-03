import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 加载数据
df = pd.read_csv("cbd_parking_availability_by_time.csv")

# 设置页面标题
st.title("墨尔本CBD车位预测")
st.markdown("选择星期几和时间，查看哪些街道更可能有空车位。")

# 用户选择输入
weekday = st.selectbox("选择星期几", sorted(df["weekday"].unique()))
hour = st.selectbox("选择时间（24小时制）", sorted(df["hour"].unique()))

# 筛选数据
filtered = df[(df["weekday"] == weekday) & (df["hour"] == hour)]

# 排序（按空车位概率）
filtered = filtered.sort_values("unoccupied_rate", ascending=False)

# 显示前10个地点的文字列表
st.subheader("推荐车位街道（按空位率排序）")
for i, row in filtered.head(10).iterrows():
    st.write(f"{row['location']} — 空车率: {row['unoccupied_rate']:.2f}")

# Folium 地图显示
m = folium.Map(location=[-37.8136, 144.9631], zoom_start=15)
for _, row in filtered.iterrows():
    lat, lon = map(float, row["location"].split(","))
    folium.CircleMarker(
        location=(lat, lon),
        radius=6,
        fill=True,
        fill_opacity=0.7,
        popup=f"空车率: {row['unoccupied_rate']:.2f}",
        color="green" if row["unoccupied_rate"] > 0.6 else "orange",
    ).add_to(m)

st.subheader("地图可视化")
st_data = st_folium(m, width=700, height=500)
