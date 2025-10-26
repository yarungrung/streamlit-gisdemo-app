import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import leafmap.foliumap as leafmap 
import requests

st.set_page_config(layout="wide")
st.title("Leafmap與Geopandas-向量(Vector)")

# --- 選擇底圖 ---
with st.sidebar:
    st.header("地圖設定")
    option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案 ---
url = "https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json"
data = requests.get(url).json()
df = pd.DataFrame(data["result"]["records"])

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # 從 JSON 結構中提取站點資料
    records = data["result"]["records"]
    df = pd.DataFrame(records)

    st.info(f"📥 成功載入 {len(df)} 筆桃園市 YouBike 站點資料")

except Exception as e:
    st.error(f"⚠️ 無法載入桃園市 YouBike JSON 資料：{e}")
    st.stop()


# --- 2. 將經緯度轉換為 geometry ---
try:
    # 將 lat / lng 轉成數值型態
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    df.dropna(subset=["lat", "lng"], inplace=True)

    # 建立幾何點位
    geometry = [Point(xy) for xy in zip(df["lng"], df["lat"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    if gdf.empty:
        st.warning("⚠️ GeoDataFrame 為空，請檢查 JSON 經緯度欄位。")
        st.stop()

    st.success(f"✅ GeoDataFrame 建立成功，共 {len(gdf)} 個站點。")

except Exception as e:
    st.error(f"⚠️ 經緯度轉換失敗：{e}")
    st.stop()

# --- 3.建立地圖 --
m = leafmap.Map(center=[0, 0], zoom=2)

#加入向量圖層(GDF)
m.add_gdf(
    gdf,
    layer_name="youbike站點資訊",
    # 設置標記的樣式
    marker_kwds={
        "radius": 6, 
        "color": "#007BFF", 
        "fill": True, 
        "fillColor": "#007BFF", 
        "fillOpacity": 0.8
    },
)

#5.互動控制及顯示地圖
m.add_layer_control()
m.to_streamlit(height=700)