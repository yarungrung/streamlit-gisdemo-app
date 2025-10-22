import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")
st.title("Leafmap - 向量(Vector) + 網格(Raster)")

# 把Widgets放到側邊攔(sidebar)
with st.sidebar:
 st.header("這裡是側邊攔")
 #選擇框
option = st.selectbox(
"選擇底圖(Basemap),
("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter")
) 

# --- 1. 網格資料(COG)---
# 線上的SRTM DEM (全球數值高程模型)
cog_url = 
"https://github.com/opengeos/leafmap/raw/master/examples/data/cog.tif"

# --- 2.向量資料 (GDF) --
url = 
"https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zi
 p"
 gdf = gpd.read_file(url)

# --- 3.建立地圖 --
m = leafmap.Map(center=[0, 0], zoom=2)
# --- 4. 加入圖層 --
# 加入網格圖層(COG)
m.add_raster(
 cog_url,
 palette="terrain", #使用"terrain"(地形)調色盤 
 layer_name="Global DEM (Raster)"
 )

#加入向量圖層(GDF)
m.add_gdf(
 gdf,
 layer_name="全球國界(Vector)" 
 style={"fillOpacity": 0, "color": "black", "weight": 0.5} # 設為透明，只留邊界
)

#5.互動控制
m.add_layer_control()
m.to_streamlit(height=700)