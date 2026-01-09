import os
import subprocess
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from yt_dlp import YoutubeDL

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Video Unique-ifier is Online!"}

@app.get("/process")
def process_video(video_url: str = Query(...)):
    input_file = "input.mp4"
    output_file = "unique_video.mp4"

    try:
        # 1. Video Download karna (yt-dlp use karke)
        ydl_opts = {
            'format': 'best',
            'outtmpl': input_file,
            'noplaylist': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # 2. FFmpeg ka jadu (Copyright protection bypass logic)
        # Isme hum video ko flip karenge, speed 5% badhayenge aur color change karenge
        cmd = [
            'ffmpeg', '-y', '-i', input_file,
            '-vf', "hflip,setpts=0.95*PTS,eq=brightness=0.05:saturation=1.2",
            '-af', "atempo=1.05",
            output_file
        ]
        subprocess.run(cmd, check=True)

        # 3. Processed video file wapis bhejna
        return FileResponse(output_file, media_type='video/mp4', filename="final_video.mp4")

    except Exception as e:
        return {"error": str(e)}
    finally:
        # Purani files saaf karna (storage bachane ke liye)
        if os.path.exists(input_file): os.remove(input_file)al mein hum file link bhejenge
    return {"status": "Processing Started", "url": video_url}
