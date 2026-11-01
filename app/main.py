from fastapi import FastAPI
from app.schemas import ReviewRequest
app=FastAPI(title="AI code Reviewer")

@app.get("/health")
def health():
    return{"status":"ok"}

@app.post("/review")
def review(request: ReviewRequest):
    return{"message":"recieved",
           "repo_url":str(request.repo_url)}