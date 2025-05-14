import streamlit as st
import rawpy
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="LapRaS v2.1.1 α", layout="wide")
st.markdown("<style>html, body, [class*='css']  { font-family: 'Meiryo', sans-serif; }</style>", unsafe_allow_html=True)
st.title("LapRaS v2.1.1 α - AIベストショット選定")

uploaded_files = st.file_uploader("写真をアップロード（RAW / JPEG）", type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"], accept_multiple_files=True)
grid_options = st.selectbox("表示枚数（1行）", [2, 4, 6], index=1)

def convert_raw(file):
    try:
        with rawpy.imread(file) as raw:
            rgb = raw.postprocess(use_camera_wb=True, output_bps=8)
            img = Image.fromarray(rgb)
            img.thumbnail((800, 800))
            return img
    except Exception:
        return None

def get_focus_score(img):
    try:
        gray = np.array(img.convert("L"))
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    except:
        return 0

def get_comment(score):
    if score >= 100:
        return "ピント良好。表情も自然でバランスの取れた一枚です。"
    elif score >= 50:
        return "ややピントが甘いですが、雰囲気は悪くありません。"
    else:
        return "ピントが甘めで、再撮影をおすすめします。"

def score_color(score):
    if score >= 100:
        return "green"
    elif score >= 50:
        return "orange"
    return "red"

if uploaded_files:
    st.success(f"{len(uploaded_files)} 枚の画像を受信しました")
    rows = [uploaded_files[i:i + grid_options] for i in range(0, len(uploaded_files), grid_options)]
    for row in rows:
        cols = st.columns(len(row))
        for col, file in zip(cols, row):
            if file.name.lower().endswith(("nef", "cr2", "arw", "dng")):
                img = convert_raw(file)
            else:
                img = Image.open(file)
                img.thumbnail((800, 800))
            if img:
                score = get_focus_score(img)
                with col:
                    st.markdown(f"<div style='border: 4px solid {score_color(score)}; padding: 3px;'>", unsafe_allow_html=True)
                    st.image(img, caption=f"{file.name}（ピントスコア: {score:.1f}）", use_container_width=True)
                    st.markdown(f"> {get_comment(score)}")
                    st.checkbox("この写真を選ぶ", key=file.name)
                    st.markdown("</div>", unsafe_allow_html=True)
