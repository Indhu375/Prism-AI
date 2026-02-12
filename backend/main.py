from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Initialize Groq Client
client = Groq(api_key=os.getenv("API_KEY"))


# ─── Request Models ──────────────────────────────────────────────────────────
class BlogRequest(BaseModel):
    product_name: str
    tone: str
    word_count: int


class VideoRequest(BaseModel):
    product_name: str
    tone: str
    word_count: int
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
def generate_blog(request: BlogRequest):
    """Generate an SEO-optimized blog article."""
    try:
        prompt = f"""
You are a professional SEO blog writer.

Write a high-quality, engaging, and SEO-optimized blog article using the following details:

Product Name: {request.product_name}
Tone: {request.tone}
Word Count: Approximately {request.word_count} words

Follow this structure STRICTLY:

Title:
<SEO optimized title about the product>

Meta Description:
<150-160 characters meta description>

Introduction:
<Engaging hook-based introduction about the product>

Main Content:
<Use H2 and H3 headings properly>
<Cover product features, benefits, and use cases>
<Make content informative and structured>

Conclusion:
<Strong summary>

Call To Action:
<Encourage reader action clearly>
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional content strategist."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        generated_text = response.choices[0].message.content

        return {
            "status": "success",
            "product_name": request.product_name,
            "tone": request.tone,
            "word_count": request.word_count,
            "generated_blog": generated_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-video-script")
def generate_video_script(request: VideoRequest):
    """Generate an engaging video script."""
    try:
        prompt = f"""
You are a professional video script writer and content strategist.

Create a highly engaging and structured video script using the following details:

Product Name: {request.product_name}
Tone: {request.tone}
Duration: {request.duration}

Follow this structure STRICTLY:

Hook (First 5-10 seconds):
<Powerful attention-grabbing opening about the product>

Introduction:
<Brief intro to the product and what the video will cover>

Main Content:
<Cover product features, benefits, and use cases>
<Use storytelling or real-world examples>
<Keep pacing appropriate for {request.duration} video>

Engagement Prompt:
<Ask viewers to comment, like, and share>

Call To Action:
<Clear CTA — try the product, visit the website, etc.>

Outro:
<Strong memorable closing line>

Important: Make sure the script feels natural when spoken aloud and fits within a {request.duration} video.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional video script creator."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        generated_script = response.choices[0].message.content

        return {
            "status": "success",
            "product_name": request.product_name,
            "tone": request.tone,
            "duration": request.duration,
            "generated_script": generated_script,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Entry Point ──────────────────────────────────────────────────────────────
# to run : python -m uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)