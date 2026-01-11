from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server is Live"}

@app.get("/process")
def process_video(video_url: str):
    try:
        # Link ko theek karna
        if video_url.startswith('//'):
            video_url = 'https:' + video_url
            
        ydl_opts = {'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
        return RedirectResponse(url=download_url)
    except Exception as e:
        return {"error": str(e)}
