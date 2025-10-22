import streamlit as st
import pandas as pd

st.title("Streamlit核心Widgets")

# 1.把Widgets放到側邊攔(sidebar)
with st.sidebar:
 st.header("這裡是側邊攔")
 
# 選擇框(Selectbox)
option = st.selectbox(
 "你最喜歡的GIS軟體?",
 ("QGIS", "ArcGIS", "ENVI", "GRASS")
 )
 
 # 滑桿(Slider)
year = st.slider("選擇一個年份:", 1990, 2030, 2024)
 
st.write(f"軟體: {option}")
st.write(f"年分: {year}")
 
 # 按鈕(Button)
if st.button("氣球!"):
 st.balloons()
 
 #檔案上傳((File Uploader)
 uploaded_file = st.file_uploader(
 "上傳Shapefile (.zip)或 GeoTIFF (.tif) 或 GeoJSON (.json)",
 type=["zip", "tif", "json"]
 )

 if uploaded_file is not None:
  st.success(f"上傳了: {uploaded_file.name} (大小: {uploaded_file.size} bytes)")