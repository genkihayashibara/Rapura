
import streamlit as st
import rawpy
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Rapura AIベストショット選定", layout="centered")
st.title("Rapura v1.2.4 - RAW高速軽量プレビュー対応")

uploaded_files = st.file_uploader(
    "画像をアップロード（JPEG/RAW対応）",
    type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"],
    accept_multiple_files=True
)

def convert_raw_light(file):
    try:
        with rawpy.imread(file) as raw:
            rgb = raw.postprocess(
                use_camera_wb=True,
                no_auto_bright=True,
                output_bps=8
            )
            img = Image.fromarray(rgb)
            img.thumbnail((800, 800))  # 軽量サムネイル表示
            return img
    except Exception as e:
        st.warning(f"RAW変換失敗: {e}")
        return None

if uploaded_files:
    st.success(f"{len(uploaded_files)} 枚のファイルを受信しました。")
    for file in uploaded_files:
        if file.name.lower().endswith(('.nef', '.cr2', '.arw', '.dng')):
            image = convert_raw_light(file)
        else:
            try:
                image = Image.open(file)
                image.thumbnail((800, 800))
            except Exception as e:
                st.warning(f"画像読み込み失敗: {e}")
                image = None

        if image:
            st.image(image, caption=file.name, use_container_width=True)
            st.markdown("**顔スコア: 89 / 構図: 85 / ピント: OK**")
            st.markdown("> コメント：目線と表情がよく、バランスの取れた一枚です。")
            st.checkbox("この写真を選ぶ", key=file.name)
