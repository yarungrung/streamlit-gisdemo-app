import streamlit as st
import pandas as pd

st.title("Streamlit  Widgets")

with st.sidebar:
 st.header("ot ")
 
 #  (Selectbox)
 option = st.selectbox(
 "o ÝöGIS ?",
 ("QGIS", "ArcGIS", "ENVI", "GRASS")
 )
 
 #  (Slider)
 year = st.slider(" :", 1990, 2030, 2024)
 
st.write(f"軟體: {option}")
 st.write(f"年分: {year}")
 
 #  (Button)
 if st.button("氣球!"):
 st.balloons()
 
 uploaded_file = st.file_uploader(
 "上傳Shapefile (.zip)或 GeoTIFF (.tif) 或 GeoJSON (.json)",
 type=["zip", "tif", "json"]
 )

 if uploaded_file is not None:
 st.success(f"
上傳了: {uploaded_file.name} (大小: {uploaded_file.size} bytes)")