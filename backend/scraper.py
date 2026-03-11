import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from models import PageMetrics


CTA_KEYWORDS = [
    "get started", "contact us", "request a quote", "learn more", "sign up",
    "schedule a call", "book a demo", "try free", "get a quote", "start now",
    "see pricing", "watch demo", "download", "subscribe", "get in touch"
]


def extract_metrics(url: str) -> tuple[PageMetrics, str]:
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.text, "html.parser")
    parsed_base = urlparse(url)

    body_text = soup.get_text(separator=" ", strip=True)
    word_count = len(body_text.split())

    h1_count = len(soup.find_all("h1"))
    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))

    cta_count = 0
    for tag in soup.find_all(["a", "button"]):
        text = tag.get_text(strip=True).lower()
        if any(kw in text for kw in CTA_KEYWORDS):
            cta_count += 1

    internal_links = 0
    external_links = 0
    for a in soup.find_all("a", href=True):
        href = a["href"]
        absolute = urljoin(url, href)
        parsed_href = urlparse(absolute)
        if parsed_href.netloc == parsed_base.netloc:
            internal_links += 1
        else:
            external_links += 1

    images = soup.find_all("img")
    image_count = len(images)
    missing_alt = sum(1 for img in images if not img.get("alt", "").strip())
    images_missing_alt_pct = round((missing_alt / image_count * 100), 1) if image_count > 0 else 0.0

    meta_title_tag = soup.find("title")
    meta_title = meta_title_tag.get_text(strip=True) if meta_title_tag else None

    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_desc_tag.get("content", "").strip() if meta_desc_tag else None

    metrics = PageMetrics(
        url=url,
        word_count=word_count,
        h1_count=h1_count,
        h2_count=h2_count,
        h3_count=h3_count,
        cta_count=cta_count,
        internal_links=internal_links,
        external_links=external_links,
        image_count=image_count,
        images_missing_alt_pct=images_missing_alt_pct,
        meta_title=meta_title,
        meta_description=meta_description,
    )

    return metrics, body_text
