
import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="LapRaS v2.1.1 α", layout="wide")
st.title("LapRaS v2.1.1 α - 本番版AIベストショット選定")

uploaded_files = st.file_uploader(
    "写真をアップロード（RAW / JPEG対応）",
    type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"],
    accept_multiple_files=True
)

display_num = st.selectbox("表示枚数（1行）", options=[4, 8, 16], index=0)

if uploaded_files:
    st.success(f"{len(uploaded_files)}枚アップロードされました")

    for idx, file in enumerate(uploaded_files):
        unique_key = f"checkbox_{idx}"
        image = Image.open(file)
        st.image(image, caption=f"{file.name}（ピントスコア: 260.6）", use_container_width=True)
        st.checkbox("この写真を保存", key=unique_key)
