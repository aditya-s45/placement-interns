from __future__ import annotations
from ..models import Job
from ..net import Net

async def fetch(company: dict, net: Net) -> list[Job]:
    url = "https://jobs.uber.com/en/"
    page = await net.fetch_html(url)
    if not page:
        return []
        
    jobs: list[Job] = []
    job_elements = page.find_all('a')
    for el in job_elements:
        try:
            link = el.get('href', '')
            if '/jobs/' in link or 'job_id=' in link:
                title = el.get_text(strip=True)
                if title:
                    job_id = link.split("/")[-1] if link else ""
                    job_url = f"https://jobs.uber.com{link}" if link.startswith("/") else link
                    jobs.append(
                        Job(
                            id=f"uber:{job_id}",
                            source="uber",
                            company=company["name"],
                            company_slug=company["slug"],
                            title=title,
                            location="Various",
                            url=job_url,
                            posted_at=None
                        )
                    )
        except Exception:
            pass
    return jobs
