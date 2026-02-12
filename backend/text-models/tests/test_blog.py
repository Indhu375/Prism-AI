from text_models.blog.blog_generator import generate_blog
from text_models.blog.schema import BlogInput

data = BlogInput(
    description="AI-powered note summarizer for students",
    category="EdTech SaaS",
    tone="Professional",
    audience="College students",
    keywords=["AI notes", "study tools", "exam preparation"]
)

print(generate_blog(data))
