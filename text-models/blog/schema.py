from pydantic import BaseModel
from typing import List

class BlogInput(BaseModel):
    description: str
    category: str
    tone: str
    audience: str
    keywords: List[str]
