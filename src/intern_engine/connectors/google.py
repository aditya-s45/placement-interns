from __future__ import annotations

from bs4 import BeautifulSoup
from ..models import Job
from ..net import Net

async def fetch(company: dict, net: Net) -> list[Job]:
    """Fetch jobs from Google Careers using standard HTTP."""
    jobs: list[Job] = []
    queries = ["intern", "apprentice"]
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    for q in queries:
        url = f"https://www.google.com/about/careers/applications/jobs/results/?q={q}"
        try:
            resp = await net.get(url, headers=headers)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            job_elements = soup.select(".VfPpkd-WsjYwc")
            for el in job_elements:
                try:
                    title_el = el.select_one("h3")
                    title = title_el.get_text(strip=True) if title_el else "Unknown"
                    link_el = el.select_one("a")
                    link = link_el.get("href", "") if link_el else ""
                    job_url = f"https://www.google.com/about/careers/applications{link}" if link.startswith("/") else link
                    loc_el = el.select_one(".pwO9Dc")
                    location = loc_el.get_text(strip=True) if loc_el else ""
                    job_id = link.split("/")[-1] if link else None
                    if not job_id or title == "Unknown":
                        continue
                    jobs.append(
                        Job(
                            id=f"google:{job_id}",
                            source="google",
                            company=company["name"],
                            company_slug=company["slug"],
                            title=title,
                            location=location,
                            url=job_url,
                            posted_at=None,
                        )
                    )
                except Exception:
                    continue
        except Exception as e:
            print(f"Failed to fetch Google {q}: {e}")

    unique = {j.id: j for j in jobs}
    return list(unique.values())
