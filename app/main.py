from fastapi import FastAPI

app=FastAPI(title="AI code Reviewer")

@app.get("/health")
def health():
    return{"status":"ok"}