from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Server is Live"}

@app.get("/process")
def process_video(video_url: str):
    return {
        "status": "success",
        "message": "Video link received",
        "received_url": video_url
    }
