# AI-Powered Website Audit Tool

An internal AI tool built for **EIGHT25MEDIA** to quickly evaluate marketing webpages and identify improvement opportunities across SEO, conversion optimization, content clarity, and UX.

**Live Demo:** [https://website-audit-backend-dhg9.onrender.com](https://website-audit-backend-dhg9.onrender.com) (backend API)

---

## What It Does

Accepts a single URL → extracts factual metrics → sends structured data to an AI model → returns prioritized insights and recommendations.

The tool is intentionally scoped to a **single page audit** with clean separation between data extraction and AI analysis.

---

## Architecture

```
URL Input
  ↓
scraper.py        →  Extracts 7 factual metrics from the page (no AI)
  ↓
models.py         →  Validates and structures data via Pydantic
  ↓
analyzer.py       →  Formats data → builds prompt → calls Groq API
  ↓
main.py           →  FastAPI orchestrates the pipeline, returns AuditResponse
  ↓
React Frontend    →  Renders 3 panels: Metrics | AI Insights | Prompt Logs
```

---

## Factual Metrics Extracted

| Metric | Description |
|---|---|
| Word Count | Total visible words on the page |
| Heading Counts | H1, H2, H3 tag counts |
| CTA Count | Buttons and primary action links |
| Internal Links | Links pointing within the same domain |
| External Links | Links pointing to other domains |
| Image Count | Total images on the page |
| Images Missing Alt Text | Percentage of images without alt attributes |
| Meta Title | Page title tag content |
| Meta Description | Meta description tag content |

---

## AI Analysis (via Groq — LLaMA 3.3 70B)

All insights are grounded in the extracted metrics. The AI covers:

1. **SEO Structure** — heading hierarchy, meta tags, link signals
2. **Messaging Clarity** — word count, content focus, value proposition
3. **CTA Usage** — conversion prompt density and placement
4. **Content Depth** — content volume relative to page purpose
5. **UX / Structural Concerns** — accessibility, structural red flags

Plus **3–5 prioritized recommendations** with reasoning tied directly to the metrics.

---

## Prompt Logs

Every audit exposes the full AI trace:
- System prompt used
- Constructed user prompt with injected metrics
- Raw model output before formatting

This provides full visibility into how the AI layer is orchestrated.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI |
| Scraping | requests + BeautifulSoup4 |
| AI | Groq API (llama-3.3-70b-versatile) |
| Data Validation | Pydantic v2 |
| Frontend | React + Tailwind CSS |

---

## Project Structure

```
AI_powered_website_audit_tool/
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── scraper.py        # Page fetching & metric extraction
│   ├── analyzer.py       # Data formatting, prompt building, AI call
│   ├── models.py         # Pydantic schemas
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── (React app)
└── .gitignore
```

---

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        
pip install -r requirements.txt
cp .env.example .env         
uvicorn main:app --reload
```

### API

```
POST /audit
Content-Type: application/json

{ "url": "https://example.com" }
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Key Design Decisions

- **Strict layer separation** — `scraper.py` never calls AI; `analyzer.py` never scrapes
- **Data-first prompting** — metrics are formatted into a structured dict before being injected into the prompt, keeping data logic and prompt logic independent
- **Structured outputs enforced** — Groq's `json_object` response format prevents malformed AI responses
- **Prompt logs as first-class output** — the full AI trace is a required part of every response, not an afterthought
- **Single API call** — one well-structured prompt rather than chained calls, reducing latency and cost

---

## Environment Variables

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com)
