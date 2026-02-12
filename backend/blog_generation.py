import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq Client
client = Groq(api_key=os.getenv("API_KEY"))


def generate_blog(product_name: str, tone: str, word_count: int, model: str = "llama-3.1-70b-versatile") -> dict:
    """
    Generate an SEO-optimized blog article for a product using Groq API.

    Args:
        product_name: Name of the product to write about
        tone: Writing tone (e.g., Professional, Casual, Informative)
        word_count: Approximate word count

    Returns:
        dict with status, metadata, and generated blog content
    """

    prompt = f"""
You are a professional SEO blog writer.

Write a high-quality, engaging, and SEO-optimized blog article about the following product:

Product Name: {product_name}
Tone: {tone}
Word Count: Approximately {word_count} words

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

    try:
        response = client.chat.completions.create(
            model=model,
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
            "product_name": product_name,
            "tone": tone,
            "word_count": word_count,
            "generated_blog": generated_text
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
