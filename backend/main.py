from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from blog_generation import generate_blog
from video_script import generate_video_script
from image_generation import generate_image, IMAGE_DIR

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

# Serve generated images as static files
app.mount("/images", StaticFiles(directory=str(IMAGE_DIR)), name="images")



# ─── Request Models ──────────────────────────────────────────────────────────
class BlogRequest(BaseModel):
    product_name: str
    tone: str
    word_count: int


class VideoRequest(BaseModel):
    product_name: str
    tone: str
    duration: str  # e.g., "60 seconds", "5 minutes"


class ImageRequest(BaseModel):
    product_name: str
    style: str  # e.g., "Minimalist", "Vibrant", "Corporate", "Futuristic"
    platform: str  # e.g., "Instagram", "LinkedIn", "Twitter"


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {
        "message": "Prism AI is Running 🚀",
        "docs": "/docs",
        "endpoints": {
            "generate_blog": "/generate-blog",
            "generate_video_script": "/generate-video-script",
            "generate_image": "/generate-image",
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


@app.post("/generate-image")
def create_image(request: ImageRequest):
    """Generate a social media image for a product using image_generation.py"""
    result = generate_image(
        product_name=request.product_name,
        style=request.style,
        platform=request.platform,
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return result


# ─── Entry Point ──────────────────────────────────────────────────────────────
# to run : python -m uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)