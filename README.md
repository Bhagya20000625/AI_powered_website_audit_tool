# AI-Powered Website Audit Tool

An internal AI tool built for **EIGHT25MEDIA** to quickly evaluate marketing webpages and identify improvement opportunities across SEO, conversion optimization, content clarity, and UX.

**Live Demo:** [https://ai-powered-website-audit-tool-j4zersh0y.vercel.app](https://ai-powered-website-audit-tool-j4zersh0y.vercel.app) (frontend)
**Backend API:** [https://website-audit-backend-dhg9.onrender.com](https://website-audit-backend-dhg9.onrender.com)

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

## Trade-offs

- **Single page only** — the tool audits one URL at a time with no crawling. This keeps the scope tight and the output focused, but means it can't assess site-wide patterns like internal linking structure across pages.
- **Static scraping only** — uses `requests` + `BeautifulSoup`, so JavaScript-rendered content is not captured. Pages that rely heavily on client-side rendering will return incomplete metrics.
- **No caching** — every audit makes a fresh scrape and a fresh AI call. For a demo tool this is fine, but at scale it would be inefficient for repeated audits of the same URL.
- **LLM non-determinism** — even at temperature 0.3, AI output varies slightly between runs. Insights are grounded in metrics but phrasing and emphasis can shift. A production version would benefit from evaluation/validation against known benchmarks.
- **Free tier constraints** — both Render (backend) and Groq (AI) are on free tiers, which means cold start delays on Render and rate limits on the AI. Acceptable for a submission, not for production.

---

## What I Would Improve With More Time

- **Pre-launch competitive readiness audit** — benchmark a new site directly against a competitor before going live, answering *"Are we ready to compete?"* rather than just *"Are we ready to launch?"* See the full concept below.
- **AI-powered candidate screening** — apply the same audit engine to hiring: paste a portfolio URL + job requirements and receive a structured fit report with skill gaps and an overall match score. See the full concept below.
- **JavaScript rendering** — integrate Playwright or Puppeteer to handle SPAs and dynamically loaded content, capturing the full page as a user sees it
- **Multi-page crawling** — extend the scraper to crawl a configurable depth, enabling site-wide audits and cross-page analysis (e.g. duplicate H1s, orphaned pages)
- **Audit history** — persist results to a database so users can track improvements over time and compare audits across dates
- **Confidence scoring** — add a signal on each AI insight indicating how strongly it is supported by the extracted metrics, making it easier to prioritise findings
- **Custom prompt profiles** — allow users to select an audit focus (e.g. SEO-heavy vs conversion-focused) which adjusts the system prompt weighting accordingly
- **Structured evals** — build a lightweight evaluation harness to test prompt quality against a set of known pages, catching regressions when the prompt or model changes

---

## Future Vision — AI-Powered Candidate Screening

Another extension is applying the same audit engine to EIGHT25MEDIA's hiring process. A hiring manager pastes a candidate's portfolio URL alongside job requirements and receives a structured fit report:

| Category | Score |
|---|---|
| Technical Skills Match | 78% |
| Project Relevance | 65% |
| Experience Level Fit | 82% |
| Missing Requirements | React, AWS |
| **Overall Fit Score** | **75 / 100** |

Followed by an AI-generated summary explaining exact gaps and recommended interview focus areas.

**Why it matters for EIGHT25MEDIA:**
- Saves hours of manual portfolio review per open role
- Ranks candidates against the same structured criteria, reducing bias
- Highlights exact skill gaps so interviewers know what to probe
- Scales effortlessly from 5 to 50 candidates with the same effort

---

## Future Vision — Pre-Launch Competitive Readiness Audit

A natural evolution of the single-page audit is a **Pre-Launch Competitive Readiness Audit** — benchmarking a new site directly against its top competitor before going live. Rather than asking *"Is it ready to launch?"*, the more valuable question is: *"Are we ready to compete?"*

**Side-by-Side Metric Comparison:**

| Metric | Your Site | Competitor | Status |
|---|---|---|---|
| Word Count | 620 | 1,400 | ⚠️ Fix before launch |
| H2 Count | 3 | 9 | ⚠️ Fix before launch |
| CTA Count | 2 | 6 | ⚠️ Fix before launch |
| Images Missing Alt | 40% | 5% | ❌ Critical — fix now |
| Meta Description | Missing | Present | ❌ Critical — fix now |
| Internal Links | 8 | 7 | ✅ Competitive |

**Launch Readiness Score: 58/100 — Not Ready**

**Why this is more valuable than a standard pre-launch checklist:**
A generic checklist tells you if something exists. This tool tells you if what exists is good enough to win. For a web agency like EIGHT25MEDIA, that distinction is everything — clients don't just want a working website, they want a website that outperforms their competition from day one. This feature gives EIGHT25MEDIA a concrete, data-backed conversation with clients about why certain elements need more investment before launch, removing the subjectivity from those discussions entirely.

---

## Environment Variables

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com)
