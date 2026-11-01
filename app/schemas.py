from pydantic import BaseModel, HttpUrl

class ReviewRequest(BaseModel):
    repo_url: HttpUrl