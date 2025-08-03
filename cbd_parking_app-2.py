
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 页面标题和说明
st.title("墨尔本CBD车位预测")
st.write("选择星期几和时间，查看哪些街道更可能有空车位。")

# 读取数据
df = pd.read_csv("cbd_parking_availability_by_time.csv")

# 用户输入控件
weekday = st.selectbox("选择星期几", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
hour = st.selectbox("选择时间（24小时制）", list(range(0, 24)))

# 筛选数据
filtered = df[(df["weekday"] == weekday) & (df["hour"] == hour)]

# 排序，空车位率高的在上
filtered = filtered.sort_values("unoccupied_rate", ascending=False)

# 创建地图
if not filtered.empty:
    lat, lon = -37.8136, 144.9631  # 墨尔本CBD中心点
    m = folium.Map(location=[lat, lon], zoom_start=15)

    for _, row in filtered.iterrows():
        location_parts = row["location"].strip("()").split(",")
        if len(location_parts) == 2:
            try:
                lat = float(location_parts[0])
                lon = float(location_parts[1])
                popup_text = f"空车位率: {row['unoccupied_rate']:.2f}"
                folium.Marker([lat, lon], popup=popup_text).add_to(m)
            except ValueError:
                continue

    st_folium(m, width=700, height=500)
else:
    st.warning("没有找到符合条件的数据，请尝试选择其他时间或星期。")
