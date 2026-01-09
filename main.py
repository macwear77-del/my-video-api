import os
import subprocess
from fastapi import FastAPI, BackgroundTasks
from yt_dlp import YoutubeDL

app = FastAPI()

# Video download aur edit karne ka function
def process_video(url, output_name):
    # 1. Download
    ydl_opts = {'format': 'best', 'outtmpl': 'input_video.mp4'}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # 2. Edit (FFmpeg use karke speed aur color change karna)
    # Ye command video ko 5% fast karega aur mirror (flip) kar dega
    cmd = [
        'ffmpeg', '-i', 'input_video.mp4',
        '-vf', 'hflip,setpts=0.95*PTS,eq=brightness=0.05:saturation=1.2', 
        '-af', 'atempo=1.05', 
        output_name
    ]
    subprocess.run(cmd)
    
    # Purani file delete karna
    if os.path.exists("input_video.mp4"):
        os.remove("input_video.mp4")

@app.get("/")
def home():
    return {"message": "Video Processor is Running Free!"}

@app.get("/process")
def start_processing(video_url: str):
    # Ye sirf testing ke liye hai, real mein hum file link bhejenge
    return {"status": "Processing Started", "url": video_url}
