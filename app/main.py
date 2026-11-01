import subprocess

from fastapi import FastAPI, HTTPException

from app.pipeline import run_review
from app.schemas import Finding, ReviewRequest

app = FastAPI(title="AI Code Reviewer")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/review", response_model=list[Finding])
def review(request: ReviewRequest):
    try:
        return run_review(str(request.repo_url), request.use_llm)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        raise HTTPException(
            status_code=400, detail="Could not clone the repository"
        ) from err