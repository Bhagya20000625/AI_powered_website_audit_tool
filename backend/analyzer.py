import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from models import PageMetrics, AIInsights, Recommendation, PromptLog

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

SYSTEM_PROMPT = """You are a senior web strategist and SEO analyst working for EIGHT25MEDIA,
a marketing agency specializing in high-performing marketing websites focused on SEO,
conversion optimization, content clarity, and UX.

You will receive the following factual webpage metrics:
- Word count
- Number of H1, H2, H3 headings
- CTA count (buttons or primary action links)
- Internal links and external links count
- Total images and percentage missing alt text
- Meta title and meta description

Using these metrics and the provided page content, produce a structured audit covering:
1. SEO Structure
2. Messaging Clarity
3. CTA Usage
4. Content Depth
5. UX or Structural Concerns

Rules:
- Every insight MUST reference specific numbers from the provided metrics
- Be specific and non-generic — no boilerplate advice
- If a metric is missing or unclear, do not assume or guess values — base analysis only on the data provided
- Each insight must be 2–4 sentences maximum
- Provide exactly 3 to 5 prioritized recommendations, each concise but actionable
- Each recommendation must include clear reasoning tied directly to the extracted metrics
- Return ONLY valid JSON — no markdown, no explanation outside the JSON

Return this exact JSON structure:
{
  "insights": {
    "seo_structure": "...",
    "messaging_clarity": "...",
    "cta_usage": "...",
    "content_depth": "...",
    "ux_concerns": "..."
  },
  "recommendations": [
    {
      "priority": 1,
      "recommendation": "...",
      "reasoning": "..."
    },
    {
      "priority": 2,
      "recommendation": "...",
      "reasoning": "..."
    },
    {
      "priority": 3,
      "recommendation": "...",
      "reasoning": "..."
    }
  ]
}"""


def format_metrics_for_prompt(metrics: PageMetrics) -> dict:
    return {
        "url": metrics.url,
        "word_count": metrics.word_count,
        "h1_count": metrics.h1_count,
        "h2_count": metrics.h2_count,
        "h3_count": metrics.h3_count,
        "cta_count": metrics.cta_count,
        "internal_links": metrics.internal_links,
        "external_links": metrics.external_links,
        "image_count": metrics.image_count,
        "images_missing_alt_pct": metrics.images_missing_alt_pct,
        "meta_title": metrics.meta_title or "MISSING",
        "meta_description": metrics.meta_description or "MISSING",
    }


def build_user_prompt(formatted: dict, page_text: str) -> str:
    return f"""Audit the following webpage.

## Extracted Metrics
- URL: {formatted["url"]}
- Word Count: {formatted["word_count"]}
- H1 Count: {formatted["h1_count"]}
- H2 Count: {formatted["h2_count"]}
- H3 Count: {formatted["h3_count"]}
- CTA Count: {formatted["cta_count"]}
- Internal Links: {formatted["internal_links"]}
- External Links: {formatted["external_links"]}
- Total Images: {formatted["image_count"]}
- Images Missing Alt Text: {formatted["images_missing_alt_pct"]}%
- Meta Title: {formatted["meta_title"]}
- Meta Description: {formatted["meta_description"]}

## Page Content (first 3000 characters)
{page_text[:3000]}

Based strictly on the metrics above, provide the structured audit in the required JSON format."""


def analyze(metrics: PageMetrics, page_text: str) -> tuple[AIInsights, list[Recommendation], PromptLog]:
    formatted = format_metrics_for_prompt(metrics)
    user_prompt = build_user_prompt(formatted, page_text)

    response = model.generate_content(
        f"{SYSTEM_PROMPT}\n\n{user_prompt}",
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json",
        ),
    )

    raw_output = response.text

    data = json.loads(raw_output)

    insights = AIInsights(**data["insights"])
    recommendations = [Recommendation(**r) for r in data["recommendations"]]

    prompt_log = PromptLog(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        raw_model_output=raw_output,
    )

    return insights, recommendations, prompt_log