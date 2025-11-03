import streamlit as st
import subprocess
import tempfile
import os

# --- ページ設定 ---
st.set_page_config(page_title="🎥 HACKER風 YouTubeダウンローダー", page_icon="💾", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: #00FF41;
        font-family: Consolas, monospace;
    }
    .stTextInput > div > div > input {
        background-color: #001400;
        color: #00FF41;
        border: 1px solid #00FF41;
    }
    .stTextArea > div > textarea {
        background-color: #001400;
        color: #00FF41;
        border: 1px solid #00FF41;
    }
    .stButton > button {
        background-color: black;
        color: #00FF41;
        border: 1px solid #00FF41;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #001600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- タイトル ---
st.title("💾 HACKER風 YouTubeダウンローダー")

# --- 入力欄 ---
url = st.text_input("🎞️ 動画URLを入力")
quality = st.selectbox("📺 解像度", ["最高画質", "1080", "720", "480", "360"])
audio_only = st.checkbox("🎵 音声のみ（MP3）")
cookie_file = st.file_uploader("🍪 クッキーファイル（任意）", type=["txt"])

# --- 出力ログ ---
log_area = st.empty()

# --- 実行ボタン ---
if st.button("🚀 ダウンロード開始"):
    if not url.strip():
        st.error("❌ URLを入力してください。")
    else:
        with st.spinner("▶ ダウンロード中..."):
            try:
                # 一時フォルダに保存
                with tempfile.TemporaryDirectory() as tmpdir:
                    command = [
                        "yt-dlp", url,
                        "-P", tmpdir,
                        "-o", "%(title)s.%(ext)s",
                        "--embed-metadata", "--embed-thumbnail", "--add-metadata"
                    ]

                    if cookie_file is not None:
                        cookie_path = os.path.join(tmpdir, "cookies.txt")
                        with open(cookie_path, "wb") as f:
                            f.write(cookie_file.read())
                        command += ["--cookies", cookie_path]

                    if audio_only:
                        command += ["-x", "--audio-format", "mp3"]
                    else:
                        if quality != "最高画質":
                            command += ["-f", f"bv[height<={quality}]+ba/b[height<={quality}]"]
                        else:
                            command += ["-f", "bestvideo+bestaudio/best"]

                    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    st.text_area("📜 出力ログ", result.stdout + result.stderr, height=250)

                    # ファイル検出
                    files = os.listdir(tmpdir)
                    if files:
                        for f in files:
                            file_path = os.path.join(tmpdir, f)
                            with open(file_path, "rb") as data:
                                st.download_button(
                                    label=f"💾 ダウンロード: {f}",
                                    data=data,
                                    file_name=f,
                                    mime="video/mp4" if not audio_only else "audio/mpeg"
                                )
                        st.success("✅ ダウンロード完了！")
                    else:
                        st.error("❌ ファイルが見つかりませんでした。")

            except Exception as e:
                st.error(f"❌ エラー発生: {e}")
