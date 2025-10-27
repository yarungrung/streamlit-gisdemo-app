import streamlit as st
import pandas as pd
import os
import json
import geopandas as gpd
from shapely.geometry import Point
import leafmap.foliumap as leafmap 


st.set_page_config(layout="wide")
st.title("Leafmap與Geopandas-向量(Vector)")

# --- 選擇底圖 ---
with st.sidebar:
    st.header("地圖設定")
    option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取本地 JSON 檔案 ---
file_path = r"C:\桃園市政府公共自行車2.0系統即時資料.json"

if not os.path.exists(file_path):
    st.error("❌ 找不到檔案{file_path}")
    st.stop()

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"⚠️ 無法讀取 JSON 檔案：{e}")
    st.stop()

# --- 2. 解析 JSON 結構 ---
# 桃園市 YouBike JSON 結構中，實際資料通常在 "result" → "records"
try:
    records = data.get("result", {}).get("records", [])
    if not records:
        st.warning("⚠️ JSON 檔案中找不到 'records' 資料。請確認檔案內容格式。")
        st.stop()
except Exception as e:
    st.error(f"⚠️ JSON 結構解析失敗：{e}")
    st.stop()

# --- 3. 轉成 DataFrame ---
df = pd.DataFrame(records)
if df.empty:
    st.warning("⚠️ 轉換後的 DataFrame 為空。請檢查原始 JSON。")
    st.stop()

# --- 4. 經緯度欄位轉換 ---
# 桃園 YouBike 的欄位名稱應該是 "lat"、"lng"
try:
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    df.dropna(subset=["lat", "lng"], inplace=True)

    # 建立 GeoDataFrame
    geometry = [Point(xy) for xy in zip(df["lng"], df["lat"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    if gdf.empty:
        st.warning("⚠️ GeoDataFrame 為空，請確認經緯度欄位是否正確。")
        st.stop()

    st.success(f"✅ 成功載入 {len(gdf)} 個站點。")

except Exception as e:
    st.error(f"⚠️ 經緯度轉換失敗：{e}")
    st.stop()

# --- 5. 顯示地圖 ---
try:
    m = leafmap.Map(center=[24.99, 121.31], zoom=11)
    m.add_points_from_xy(
        gdf,
        x="lng",
        y="lat",
        popup=["sna", "sarea", "ar"],
        layer_name="桃園 YouBike 站點"
    )
    m.to_streamlit(height=600)

except Exception as e:
    st.error(f"⚠️ 地圖繪製失敗：{e}")
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

# --- 5. 顯示地圖 ---
m = leafmap.Map(center=[24.99, 121.31], zoom=11)
m.add_points_from_xy(
        gdf,
        x="lng",
        y="lat",
        popup=["sna", "sarea", "ar"],
        layer_name="桃園 YouBike 站點"
    )


#5.互動控制及顯示地圖
m.add_layer_control()
m.to_streamlit(height=700)