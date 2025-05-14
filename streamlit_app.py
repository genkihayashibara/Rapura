
import streamlit as st
import rawpy
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="LapRaS v2.1 - AI写真選定", layout="wide")
st.title("LapRaS v2.1 - プロ仕様AIベストショット選定")

uploaded_files = st.file_uploader(
    "写真をアップロード（RAW / JPEG）",
    type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"],
    accept_multiple_files=True
)

# グリッド枚数選択
columns_per_row = st.selectbox("1行に表示する画像数", [2, 3, 4, 6], index=2)

def convert_raw(file):
    try:
        with rawpy.imread(file) as raw:
            rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=8)
            img = Image.fromarray(rgb)
            img.thumbnail((800, 800))
            return img
    except Exception:
        return None

def get_focus_score(image: Image.Image):
    try:
        gray = np.array(image.convert("L"))
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    except Exception:
        return 0

def get_score_style(score):
    if score >= 100:
        return "5px solid green"
    elif score >= 50:
        return "5px solid orange"
    else:
        return "5px solid red"

if uploaded_files:
    st.success(f"{len(uploaded_files)} 枚のファイルを受信しました。")
    rows = [uploaded_files[i:i + columns_per_row] for i in range(0, len(uploaded_files), columns_per_row)]

    for row in rows:
        cols = st.columns(len(row))
        for col, file in zip(cols, row):
            if file.name.lower().endswith(('.nef', '.cr2', '.arw', '.dng')):
                image = convert_raw(file)
            else:
                try:
                    image = Image.open(file)
                    image.thumbnail((800, 800))
                except Exception:
                    image = None

            if image:
                focus_score = get_focus_score(image)
                border_style = get_score_style(focus_score)

                with col:
                    st.markdown(f"<div style='border:{border_style}; padding:4px'>", unsafe_allow_html=True)
                    st.image(image, caption=file.name, use_column_width='always')
                    st.markdown(f"<div>ピントスコア: {focus_score:.1f}</div>", unsafe_allow_html=True)
                    st.checkbox("この写真を保存", key=file.name)
                    st.markdown("</div>", unsafe_allow_html=True)
