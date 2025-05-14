import streamlit as st
from PIL import Image
import rawpy
import io

st.title("LapRaS 軽量RAW & JPEG プレビュー")

uploaded_files = st.file_uploader(
    "写真をアップロード（RAW / JPEG / PNG対応）",
    type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        st.markdown("---")
        st.write(f"ファイル名: {file.name}")
        if file.type.startswith("image/jpeg") or file.type.startswith("image/png"):
            img = Image.open(file)
        else:
            raw = rawpy.imread(io.BytesIO(file.read()))
            img = Image.fromarray(raw.postprocess())
        st.image(img, caption=file.name, use_container_width=True)
