
import streamlit as st
from PIL import Image
import rawpy
import io

def convert_preview(file):
    try:
        with rawpy.imread(file) as raw:
            thumb = raw.extract_thumb()
            if thumb.format == rawpy.ThumbFormat.JPEG:
                return Image.open(io.BytesIO(thumb.data))
            elif thumb.format == rawpy.ThumbFormat.BITMAP:
                return Image.fromarray(thumb.data)
    except Exception as e:
        st.error(f"変換に失敗しました: {e}")
        return None

st.title("LapRaS 軽量RAWプレビュー")
uploaded_files = st.file_uploader("写真をアップロード", type=["nef", "cr2", "arw", "dng"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.write(file.name)
        img = convert_preview(file)
        if img:
            st.image(img, caption=file.name, use_column_width=True)
