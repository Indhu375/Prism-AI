import os
import uuid
import base64
from pathlib import Path

from groq import Groq
from together import Together
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
groq_client = Groq(api_key=os.getenv("API_KEY"))
together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# Directory to save generated images
IMAGE_DIR = Path(__file__).parent / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True)

# Platform-specific image dimensions
PLATFORM_SIZES = {
    "instagram": {"width": 1080, "height": 1080},
    "linkedin": {"width": 1200, "height": 627},
    "twitter": {"width": 1200, "height": 675},
    "facebook": {"width": 1200, "height": 630},
    "youtube": {"width": 1280, "height": 720},
}


def _generate_image_prompt(product_name: str, style: str, platform: str) -> str:
    """
    Use Groq LLM to create an optimized image generation prompt
    from the product name, style, and target platform.
    """
    meta_prompt = f"""
You are an expert social media visual designer.

Generate a detailed, vivid image generation prompt for an AI image model.
The image should be a stunning social media graphic for the following:

Product Name: {product_name}
Visual Style: {style}
Target Platform: {platform}

Requirements:
- Describe colors, composition, lighting, and mood in detail
- Make it visually striking and scroll-stopping for {platform}
- Include the product name as text in the design if appropriate
- Keep the prompt under 200 words
- Do NOT include any explanations — output ONLY the image prompt

Output the image prompt directly, nothing else.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a visual design prompt engineer."},
            {"role": "user", "content": meta_prompt},
        ],
        temperature=0.8,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()


def generate_image(
    product_name: str,
    style: str,
    platform: str,
) -> dict:
    """
    Generate a social media image for a product using Together AI (FLUX model).

    The workflow:
    1. Use Groq LLM to craft an optimized image prompt
    2. Send the prompt to Together AI's FLUX model for image generation
    3. Save the resulting image locally

    Args:
        product_name: Name of the product
        style: Visual style (e.g., Minimalist, Vibrant, Corporate, Futuristic)
        platform: Target social media platform (e.g., Instagram, LinkedIn, Twitter)

    Returns:
        dict with status, metadata, image_url, and the generated prompt
    """
    try:
        # Normalize platform name
        platform_lower = platform.lower()
        dimensions = PLATFORM_SIZES.get(platform_lower, {"width": 1024, "height": 1024})

        # Step 1: Generate an optimized image prompt using Groq
        image_prompt = _generate_image_prompt(product_name, style, platform)

        # Step 2: Generate the image using Together AI FLUX model
        response = together_client.images.generate(
            prompt=image_prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=dimensions["width"],
            height=dimensions["height"],
            steps=4,
            n=1,
            response_format="b64_json",
        )

        # Step 3: Decode and save the image
        image_data = base64.b64decode(response.data[0].b64_json)
        filename = f"{product_name.replace(' ', '_').lower()}_{platform_lower}_{uuid.uuid4().hex[:8]}.png"
        filepath = IMAGE_DIR / filename

        with open(filepath, "wb") as f:
            f.write(image_data)

        # Build the URL path (will be served by FastAPI static files)
        image_url = f"/images/{filename}"

        return {
            "status": "success",
            "product_name": product_name,
            "style": style,
            "platform": platform,
            "dimensions": dimensions,
            "image_prompt": image_prompt,
            "image_url": image_url,
            "filename": filename,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
