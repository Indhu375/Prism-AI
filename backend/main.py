from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Prism AI Backend")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class GenerateRequest(BaseModel):
    description: str
    category: str
    tone: str

# Response schema
class GenerateResponse(BaseModel):
    blog: str
    video: str
    image_prompt: str

@app.get("/")
def root():
    return {"status": "Prism AI backend running"}

@app.post("/generate", response_model=GenerateResponse)
def generate_content(data: GenerateRequest):
    # 🔮 TEMP: Fake AI logic (replace later with LangChain)
    blog = (
        f"This is a {data.tone.lower()} blog post about a "
        f"{data.category.lower()} product. "
        f"{data.description}"
    )

    video = (
        "Hook: Grab attention in 3 seconds\n"
        "Problem: Describe the pain point\n"
        "Solution: Introduce the product\n"
        "CTA: Call to action"
    )

    image_prompt = (
        f"A high-quality social media banner for a "
        f"{data.category.lower()} product, "
        f"{data.tone.lower()} style"
    )

    return {
        "blog": blog,
        "video": video,
        "image_prompt": image_prompt,
    }
