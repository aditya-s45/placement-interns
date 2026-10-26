"""Internshala connector using standard HTTP requests and BeautifulSoup."""

from __future__ import annotations

import asyncio
import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
import httpx

from ..models import Job
from ..net import Net

_EXECUTOR = ThreadPoolExecutor(max_workers=2, thread_name_prefix="internshala")

_AJAX_URL = "https://internshala.com/internships_ajax/internship_list_container_ajax/{category}/page-{page}/"
_MAX_PAGES = 3
_AJAX_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
    "Referer": "https://internshala.com/internships/",
}


def _parse_html_with_bs4(html: str, category: str) -> list[Job]:
    """Parse internship cards using BeautifulSoup."""
    jobs: list[Job] = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        for card in soup.select(".individual_internship"):
            title_el = card.select_one(".profile a")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            path = title_el.get("href", "")

            comp_el = card.select_one(".company_name")
            company = comp_el.get_text(strip=True) if comp_el else "Unknown"

            loc_el = card.select_one(".location_link") or card.select_one(".location")
            location = loc_el.get_text(strip=True) if loc_el else "—"

            stipend_el = card.select_one(".stipend")
            stipend = stipend_el.get_text(strip=True) if stipend_el else None

            job_id_m = re.search(r"-([a-zA-Z0-9]+)$", path)
            job_id = job_id_m.group(1) if job_id_m else re.sub(r"[^a-z0-9]", "", path)[-12:]

            job = Job(
                id=f"internshala:{category}:{job_id}",
                source="internshala",
                company=company,
                company_slug=category,
                title=title,
                location=location,
                url=f"https://internshala.com{path}",
                posted_at=None,
            )
            if stipend:
                job.stipend = stipend  # type: ignore[attr-defined]
            jobs.append(job)
    except Exception:
        pass
    return jobs


def _fetch_page_sync(url: str) -> dict:
    """Synchronous page fetch via httpx."""
    try:
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            resp = client.get(url, headers=_AJAX_HEADERS)
            return resp.json() or {}
    except Exception:
        return {}


async def fetch(company: dict, net: Net) -> list[Job]:
    category = company["slug"]
    jobs: list[Job] = []
    loop = asyncio.get_event_loop()

    for page in range(1, _MAX_PAGES + 1):
        url = _AJAX_URL.format(category=category, page=page)
        data = await loop.run_in_executor(_EXECUTOR, _fetch_page_sync, url)

        html = data.get("html", "")
        if not html:
            break

        page_jobs = _parse_html_with_bs4(html, category)
        if not page_jobs:
            break
        jobs.extend(page_jobs)
        await asyncio.sleep(0.8)

    return jobs
