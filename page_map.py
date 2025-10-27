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
file_path = "台北市youbike.json"

if not os.path.exists(file_path):
    st.error(f"❌ 找不到 JSON 檔案：{file_path}")
    st.stop()

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ 自動偵測 JSON 結構
    if isinstance(data, dict):
        # 若是台北開放資料的格式（dict 裡面包 result → records）
        records = data.get("result", {}).get("records")
        if records is None:
            st.warning("⚠️ JSON 格式中沒有 result/records，改用最外層內容")
            records = data
    elif isinstance(data, list):
        records = data
    else:
        st.error("⚠️ JSON 結構無法辨識，請確認檔案內容")
        st.stop()

    # ✅ 轉成 DataFrame
    df = pd.DataFrame(records)
    st.success(f"✅ 成功載入 {len(df)} 筆資料！")
    st.dataframe(df.head())

except json.JSONDecodeError:
    st.error("⚠️ JSON 格式錯誤，請確認檔案內容是否完整。")
    st.stop()
except Exception as e:
    st.error(f"❌ 發生錯誤：{e}")
    st.stop()

# --- 2. 經緯度轉換 + 建立 GeoDataFrame ---"
try:
    # 自動偵測可能的經緯度欄位名稱
    possible_lat = ["lat", "latitude", "Lat", "Latitude", "LAT", "Y", "y"]
    possible_lng = ["lng", "lon", "long", "longitude", "Lng", "Longitude", "LON", "X", "x"]

    lat_col = next((col for col in df.columns if col in possible_lat), None)
    lng_col = next((col for col in df.columns if col in possible_lng), None)

    if lat_col is None or lng_col is None:
        st.error(f"❌ 找不到經緯度欄位！目前欄位：{list(df.columns)}")
        st.stop()

    df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
    df[lng_col] = pd.to_numeric(df[lng_col], errors="coerce")
    df.dropna(subset=[lat_col, lng_col], inplace=True)

    # 建立 GeoDataFrame
    geometry = [Point(xy) for xy in zip(df[lng_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    if gdf.empty:
        st.warning("⚠️ GeoDataFrame 為空，請確認經緯度欄位是否正確。")
        st.stop()

    st.success(f"✅ GeoDataFrame 建立成功，共 {len(gdf)} 個站點。")

except Exception as e:
    st.error(f"⚠️ 經緯度轉換失敗：{e}")
    st.stop()

# --- 3. 顯示地圖 ---
try:
    m = leafmap.Map(center=[24.99, 121.31], zoom=11)
    m.add_points_from_xy(
        gdf,
        x="longitude",
        y="latitude",
        popup=["sna", "sarea", "ar"],
        layer_name="台北市 YouBike 站點"
    )
    m.to_streamlit(height=600)

except Exception as e:
    st.error(f"⚠️ 地圖繪製失敗：{e}")
