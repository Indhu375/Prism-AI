"""
Prism AI — FastAPI Application Entry Point

Exposes endpoints for blog, video-script, and image generation.
"""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from config import VALID_PLATFORMS, VALID_STYLES
from blog_generation import generate_blog
from video_script import generate_video_script
from image_generation import generate_image, IMAGE_DIR

logger = logging.getLogger("prism.api")

# ─── App Setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Prism AI",
    description="AI-powered Blog, Video Script & Image Generation API",
    version="2.0.0",
)

# CORS — allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated images as static files
app.mount("/images", StaticFiles(directory=str(IMAGE_DIR)), name="images")


# ─── Request Models (with validation) ────────────────────────────────────────
class BlogRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    tone: str = Field(..., min_length=1, max_length=50, description="Writing tone")
    word_count: int = Field(..., ge=100, le=5000, description="Approximate word count (100-5000)")


class VideoRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    tone: str = Field(..., min_length=1, max_length=50, description="Writing tone")
    duration: int = Field(..., ge=1, le=30, description="Video duration in minutes (1-30)")


class ImageRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    style: VALID_STYLES = Field(..., description="Visual style for the image")
    platform: VALID_PLATFORMS = Field(..., description="Target social media platform")
    seed: int | None = Field(None, description="Optional seed for reproducible generation")
    n: int = Field(1, ge=1, le=4, description="Number of images to generate (1-4)")


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
async def home():
    return {
        "message": "Prism AI is Running 🚀",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "generate_blog": "/generate-blog",
            "generate_video_script": "/generate-video-script",
            "generate_image": "/generate-image",
        },
    }


@app.get("/health")
async def health():
    """Simple health-check endpoint."""
    return {"status": "ok"}


@app.post("/generate-blog")
async def create_blog(request: BlogRequest):
    """Generate an SEO-optimized blog article."""
    try:
        result = await generate_blog(
            product_name=request.product_name,
            tone=request.tone,
            word_count=request.word_count,
        )
        return result
    except Exception as e:
        logger.exception("Blog generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-video-script")
async def create_video_script(request: VideoRequest):
    """Generate an engaging video script."""
    try:
        result = await generate_video_script(
            product_name=request.product_name,
            tone=request.tone,
            duration_mins=request.duration,
        )
        return result
    except Exception as e:
        logger.exception("Video script generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-image")
async def create_image(request: ImageRequest):
    """Generate a social media image for a product."""
    try:
        result = await generate_image(
            product_name=request.product_name,
            style=request.style,
            platform=request.platform,
            seed=request.seed,
            n=request.n,
        )
        return result
    except Exception as e:
        logger.exception("Image generation failed")
        raise HTTPException(status_code=500, detail=str(e))


# ─── Entry Point ──────────────────────────────────────────────────────────────
# Run: python -m uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)