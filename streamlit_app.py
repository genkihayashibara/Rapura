import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Rapura AIベストショット選定", layout="centered")
st.title("Rapura v1.2.1 - AIベストショット選定")

uploaded_files = st.file_uploader(
    "画像をアップロード（JPEG/RAW対応）",
    type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} 枚のファイルを受信しました。")
    for f in uploaded_files:
        try:
            # 画像を読み込む（PILで）
            image = Image.open(f)
            st.image(image, caption=f.name, use_container_width=True)

            # 仮のAIスコア表示（ここは今後APIと接続）
            st.markdown("**顔スコア: 89 / 構図: 85 / ピント: OK**")
            st.markdown("> コメント：目線と表情がよく、バランスの取れた一枚です。")
            st.checkbox("この写真を選ぶ", key=f.name)

        except Exception as e:
            st.error(f"画像表示に失敗しました：{e}")
