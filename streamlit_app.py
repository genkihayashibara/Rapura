
import streamlit as st
import rawpy
from PIL import Image
import numpy as np

st.set_page_config(page_title="LapRaS - ラプラス本番版", layout="wide")
st.title("LapRaS v2.0.0 α - 本番版AIベストショット選定")

uploaded_files = st.file_uploader(
    "写真をアップロード（RAW / JPEG対応）",
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
            img.thumbnail((800, 800))
            return img
    except Exception as e:
        st.warning(f"RAW変換失敗: {e}")
        return None

def dummy_ai_score(filename):
    import random
    return {
        "face": random.randint(75, 100),
        "composition": random.randint(70, 95),
        "focus": random.choice(["OK", "やや甘い", "ブレ"])
    }

if uploaded_files:
    st.success(f"{len(uploaded_files)} 枚のファイルを受信しました。")

    results = []
    for file in uploaded_files:
        # RAW or JPEG読込
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
            score = dummy_ai_score(file.name)
            results.append((file.name, image, score))

    # スコア順並び替え（仮で顔スコア）
    results.sort(key=lambda x: x[2]['face'], reverse=True)

    # 表示
    for name, image, score in results:
        st.image(image, caption=name, use_container_width=True)
        st.markdown(f"**顔スコア：{score['face']} / 構図：{score['composition']} / ピント：{score['focus']}**")
        st.markdown("> コメント：自然な表情とバランスの取れた構図です。")
        st.checkbox("この写真を保存", key=name)
