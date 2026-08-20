"""Custom scraper with CSS selectors and LLM fallback for non-ATS career pages."""

from __future__ import annotations

import urllib.parse
from datetime import UTC, datetime

from ..models import Job
from ..net import Net
from ..llm import extract_jobs_from_html

async def fetch(company: dict, net: Net) -> list[Job]:
    """Fetch jobs from a custom careers page.
    
    Expects company dict to have:
    - 'slug': string identifier
    - 'name': company name
    - 'careers_url': the URL to scrape (or falls back to 'url')
    - 'css_hint': (optional) CSS selector to find job nodes
    """
    slug = company["slug"]
    url = company.get("careers_url") or company.get("url")
    if not url:
        raise ValueError(f"No careers_url or url provided for custom company {slug}")

    css_hint = company.get("css_hint")
    jobs_data = []

    try:
        html = await net.get_text(url)
    except Exception as e:
        raise ValueError(f"Failed to fetch {url}: {e}")

    # Attempt 1: BeautifulSoup + css_hint
    if css_hint:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            nodes = soup.select(css_hint)
            for node in nodes:
                # Try to find the title and link within the node
                a_tag = node if node.name == "a" else node.find("a")
                if a_tag:
                    title = a_tag.get_text(strip=True)
                    link = a_tag.get("href")
                    if title and link:
                        jobs_data.append({
                            "title": title,
                            "url": urllib.parse.urljoin(url, link),
                            "location": "—" # basic parser usually can't reliably guess location
                        })
        except ImportError:
            pass # Fall back to LLM if bs4 is missing

    # Attempt 2: Fallback to LLM extraction if CSS hint yielded 0 results
    if not jobs_data:
        jobs_data = await extract_jobs_from_html(html, company["name"], url, net)

    # Self-check: if still 0 jobs, raise error so pipeline flags it
    if not jobs_data:
        raise ValueError(f"Custom scraper returned 0 jobs for {slug}. Layout changed or no internships.")

    jobs = []
    for idx, j in enumerate(jobs_data):
        job_url = j.get("url") or ""
        # Make sure url is absolute
        if not job_url.startswith("http"):
            job_url = urllib.parse.urljoin(url, job_url)
            
        jobs.append(
            Job(
                id=f"custom:{slug}:{idx}",
                source="custom",
                company=company["name"],
                company_slug=slug,
                title=(j.get("title") or "").strip(),
                location=(j.get("location") or "—").strip() or "—",
                url=job_url,
                posted_at=None,
                description=None,
            )
        )
    return jobs
