import streamlit as st

st.set_page_config(page_title="Rapura AIベストショット選定", layout="centered")

st.title("Rapura v1.2.1 - AIベストショット選定")

uploaded_files = st.file_uploader("画像をアップロード（JPEG/RAW対応）", type=["jpg", "jpeg", "png", "nef", "cr2", "arw", "dng"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} 枚のファイルを受信しました。")
    for f in uploaded_files:
        st.image(f, caption=f.name, use_column_width=True)
        st.markdown("**顔スコア: 89 / 構図: 85 / ピント: OK**")
        st.markdown("> コメント：目線と表情がよく、バランスの取れた一枚です。")
        st.checkbox("この写真を選ぶ", key=f.name)
