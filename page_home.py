import streamlit as st
 
st.title("蔡亞蓉的運用GIS功課")
st.write("此app顯示所有桃園市youbike站點店為圖資")

 # 將MP4影片的URL傳給st.video() 
video_url = "https://i.imgur.com/1GoAB0C.mp4"
 
st.write(f"正在播放影片：{video_url}")

st.video(video_url)

 # 直接上傳照片的URL傳給st.image()
image_url = "https://i.imgur.com/uf1T4ND.png"
st.image(image_url)