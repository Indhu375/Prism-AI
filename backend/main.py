from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Prism AI - Blog Generator",
    description="AI Powered SEO Blog Generator using Groq",
    version="1.0"
)

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Request Model
class BlogRequest(BaseModel):
    topic: str
    tone: str
    target_audience: str
    word_count: int
    seo_keywords: List[str]
    language: str = "English"

# Video Script Request Model
class VideoRequest(BaseModel):
    topic: str
    platform: str  # YouTube / Instagram / LinkedIn
    target_audience: str
    duration: str  # e.g., "60 seconds", "5 minutes"
    tone: str
    language: str = "English"


# Health check route
@app.get("/")
def home():
    return {"message": "Prism AI Blog Generator is Running 🚀"}

# Blog generation route
@app.post("/generate-blog")
def generate_blog(request: BlogRequest):
    try:
        prompt = f"""
You are a professional SEO blog writer.

Write a high-quality, engaging, and SEO-optimized blog article using the following details:

Topic: {request.topic}
Tone: {request.tone}
Target Audience: {request.target_audience}
Word Count: Approximately {request.word_count} words
SEO Keywords: {", ".join(request.seo_keywords)}
Language: {request.language}

Follow this structure STRICTLY:

Title:
<SEO optimized title>

Meta Description:
<150-160 characters meta description>

Introduction:
<Engaging hook-based introduction>

Main Content:
<Use H2 and H3 headings properly>
<Include SEO keywords naturally>
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
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        generated_text = response.choices[0].message.content

        return {
            "status": "success",
            "topic": request.topic,
            "tone": request.tone,
            "word_count": request.word_count,
            "generated_blog": generated_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Video Script Generation Route
@app.post("/generate-video-script")
def generate_video_script(request: VideoRequest):
    try:
        prompt = f"""
You are a professional video script writer and content strategist.

Create a highly engaging and structured video script using the following details:

Topic: {request.topic}
Platform: {request.platform}
Target Audience: {request.target_audience}
Duration: {request.duration}
Tone: {request.tone}
Language: {request.language}

Follow this structure STRICTLY:

Hook (First 5-10 seconds):
<Powerful attention-grabbing opening>

Introduction:
<Brief intro to topic>

Main Content:
<Clear, engaging, well-paced content>
<Use storytelling or examples if suitable>

Engagement Prompt:
<Ask viewers to comment/like/share>

Call To Action:
<Clear CTA aligned to platform>

Outro:
<Strong memorable closing line>
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional video script creator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        generated_script = response.choices[0].message.content

        return {
            "status": "success",
            "topic": request.topic,
            "platform": request.platform,
            "duration": request.duration,
            "generated_script": generated_script
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# to run : python -m uvicorn main:app --reload