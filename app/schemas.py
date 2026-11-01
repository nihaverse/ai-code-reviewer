from pydantic import BaseModel, HttpUrl
from typing import Literal


class ReviewRequest(BaseModel):
    repo_url: HttpUrl
    use_llm: bool = True


class Finding(BaseModel):
    file: str
    line: int
    category: Literal["bug", "security", "style"]
    severity: Literal["low", "medium", "high"]
    rule_id: str
    message: str
    source: str  # which tool found it, e.g. "ruff"
    explanation: str | None = None
    suggested_fix: str | None = None
    confidence: float | None = None
    likely_false_positive: bool = False