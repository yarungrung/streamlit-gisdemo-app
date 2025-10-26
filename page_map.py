import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import leafmap.foliumap as leafmap 
import folium 

st.set_page_config(layout="wide")
st.title("Leafmap與Geopandas-向量(Vector)")

# --- 選擇底圖 ---
with st.sidebar:
    st.header("地圖設定")
    option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案 ---
url = "桃園市政府公共自行車2.0系統即時資料.JSON"

df = pd.read_json(url)
    
st.subheader("資料預覽 (表格)")
st.dataframe(df.head())

# --- 2. 將經緯度轉成 geometry ---
try:
    df["wgsX"] = pd.to_numeric(df["wgsX"], errors='coerce') 
    df["wgsY"] = pd.to_numeric(df["wgsY"], errors='coerce') 
    
    df.dropna(subset=['wgsX', 'wgsY'], inplace=True)

    geometry = [Point(xy) for xy in zip(df["wgsY"], df["wgsX"])] 
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    if gdf.empty:
        st.warning("⚠️ GeoDataFrame (gdf) 為空！請檢查原始 JSON 檔案中是否有有效的 'wgsX' 和 'wgsY' 數值。")
        st.stop()
        
    st.info(f"✅ GeoDataFrame 成功建立，包含 {len(gdf)} 個有效點位。")

except Exception as e:
    st.error(f"⚠️ 經緯度轉換失敗。錯誤訊息: {e}")
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