from pydantic import BaseModel
from typing import Optional


class PageMetrics(BaseModel):
    url: str
    word_count: int
    h1_count: int
    h2_count: int
    h3_count: int
    cta_count: int
    internal_links: int
    external_links: int
    image_count: int
    images_missing_alt_pct: float
    meta_title: Optional[str]
    meta_description: Optional[str]


class AIInsights(BaseModel):
    seo_structure: str
    messaging_clarity: str
    cta_usage: str
    content_depth: str
    ux_concerns: str


class Recommendation(BaseModel):
    priority: int
    recommendation: str
    reasoning: str


class PromptLog(BaseModel):
    system_prompt: str
    user_prompt: str
    raw_model_output: str


class AuditResponse(BaseModel):
    metrics: PageMetrics
    insights: AIInsights
    recommendations: list[Recommendation]
    prompt_log: PromptLog
