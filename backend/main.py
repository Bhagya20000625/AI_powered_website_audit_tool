from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from scraper import extract_metrics
from analyzer import analyze
from models import AuditResponse

app = FastAPI(title="Website Audit Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuditRequest(BaseModel):
    url: HttpUrl


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/audit", response_model=AuditResponse)
def run_audit(request: AuditRequest):
    url = str(request.url)

    try:
        metrics, page_text = extract_metrics(url)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        insights, recommendations, prompt_log = analyze(metrics, page_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

    return AuditResponse(
        metrics=metrics,
        insights=insights,
        recommendations=recommendations,
        prompt_log=prompt_log,
    )