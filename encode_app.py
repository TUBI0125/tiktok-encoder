
import os
import subprocess
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="TikTok Video Encoder – AI Bypass", layout="centered")
st.title("🚀 TikTok Video Encoder – AI Bypass Edition")

INPUT_FOLDER = "./input_videos"
OUTPUT_FOLDER = "./encoded_videos"
WATERMARK_TEXT = st.text_input("Watermark Text", value="For Education Only")

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

uploaded_files = st.file_uploader("Upload MP4 videos", type="mp4", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join(INPUT_FOLDER, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
    st.success("✅ All files uploaded successfully.")

if st.button("Start Encoding"):
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(".mp4"):
            input_path = os.path.join(INPUT_FOLDER, file_name)
            output_file = f"encoded_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
            output_path = os.path.join(OUTPUT_FOLDER, output_file)

            ffmpeg_cmd = [
                "ffmpeg", "-y", "-i", input_path,
                "-c:v", "libx264",
                "-profile:v", "baseline",
                "-level", "3.0",
                "-pix_fmt", "yuv420p",
                "-b:v", "1200k",
                "-maxrate", "1500k",
                "-bufsize", "2000k",
                "-g", "90",
                "-r", "30",
                "-an",
                "-vf",
                f"scale=576:1024,drawtext=text='{WATERMARK_TEXT}':x=if(mod(t\,5)<2\,10\,main_w-200):y=10:fontsize=16:fontcolor=white:alpha=0.25",
                "-movflags", "+faststart",
                "-metadata", "title=",
                "-metadata", "comment=",
                "-metadata", "description=",
                "-metadata", "encoder=",
                "-map_metadata", "-1",
                output_path
            ]

            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            st.success(f"✅ Encoded: {output_file}")

    st.info("✅ All videos encoded. Check the ./encoded_videos folder.")
