from pydantic import BaseModel, HttpUrl
from typing import Literal


class ReviewRequest(BaseModel):
    repo_url: HttpUrl


class Finding(BaseModel):
    file: str
    line: int
    category: Literal["bug", "security", "style"]
    severity: Literal["low", "medium", "high"]
    rule_id: str
    message: str
    source: str  # which tool found it, e.g. "ruff"