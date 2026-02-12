from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from blog_generation import generate_blog
from video_script import generate_video_script

# ─── App Setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Prism AI",
    description="AI-powered Video Script & Blog Generation API",
    version="1.0.0",
)

# CORS – allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request Models ──────────────────────────────────────────────────────────
class BlogRequest(BaseModel):
    product_name: str
    tone: str
    word_count: int


class VideoRequest(BaseModel):
    product_name: str
    tone: str
    duration: str  # e.g., "60 seconds", "5 minutes"


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {
        "message": "Prism AI is Running 🚀",
        "docs": "/docs",
        "endpoints": {
            "generate_blog": "/generate-blog",
            "generate_video_script": "/generate-video-script",
        },
    }


@app.post("/generate-blog")
def create_blog(request: BlogRequest):
    """Generate an SEO-optimized blog article using blog_generation.py"""
    result = generate_blog(
        product_name=request.product_name,
        tone=request.tone,
        word_count=request.word_count,
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@app.post("/generate-video-script")
def create_video_script(request: VideoRequest):
    """Generate an engaging video script using video_script.py"""
    result = generate_video_script(
        product_name=request.product_name,
        tone=request.tone,
        duration_mins=int(request.duration),
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return result


# ─── Entry Point ──────────────────────────────────────────────────────────────
# to run : python -m uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)