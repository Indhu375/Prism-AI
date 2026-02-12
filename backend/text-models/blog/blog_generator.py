from schema import BlogInput
from pathlib import Path
from ollama_client import call_ollama

PROMPT_PATH = Path(__file__).parent / "blog_prompt.txt"

def generate_blog(data: BlogInput) -> str:
    prompt_template = PROMPT_PATH.read_text()

    prompt = prompt_template.format(
        description=data.description,
        category=data.category,
        tone=data.tone,
        audience=data.audience,
        keywords=", ".join(data.keywords),
    )

    return call_ollama(prompt)
