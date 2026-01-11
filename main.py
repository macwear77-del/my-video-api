from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is Live"}

@app.get("/process")
def process(video_url: str):
    try:
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_link = info.get('url')
        return RedirectResponse(url=video_link)
    except Exception as e:
        return {"error": str(e)}
