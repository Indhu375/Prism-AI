from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from video_script import generate_video_script
from blog_generation import generate_blog

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


# ─── Request / Response Models ────────────────────────────────────────────────
class VideoScriptRequest(BaseModel):
    product_name: str = Field(..., example="Prism AI")
    tone: str = Field(..., example="Professional")
    duration_mins: int = Field(..., ge=1, le=60, example=5)
    model: str = Field(default="llama-3.1-70b-versatile", example="llama-3.1-70b-versatile")


class BlogRequest(BaseModel):
    product_name: str = Field(..., example="Prism AI")
    tone: str = Field(..., example="Informative")
    word_count: int = Field(..., ge=100, le=5000, example=800)
    model: str = Field(default="llama-3.1-70b-versatile", example="llama-3.1-70b-versatile")


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "Welcome to Prism AI API",
        "docs": "/docs",
        "endpoints": {
            "generate_video_script": "/api/video-script",
            "generate_blog": "/api/blog",
        },
    }


@app.post("/api/video-script")
async def create_video_script(req: VideoScriptRequest):
    """Generate a video script for a given product."""
    result = generate_video_script(
        product_name=req.product_name,
        tone=req.tone,
        duration_mins=req.duration_mins,
        model=req.model,
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@app.post("/api/blog")
async def create_blog(req: BlogRequest):
    """Generate an SEO-optimized blog article for a given product."""
    result = generate_blog(
        product_name=req.product_name,
        tone=req.tone,
        word_count=req.word_count,
        model=req.model,
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return result


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
