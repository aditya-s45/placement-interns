import urllib.parse
import httpx
from bs4 import BeautifulSoup

def find_alumni(company_name: str, college: str = 'IIIT Lucknow', limit: int = 2) -> list:
    query = urllib.parse.quote(f'site:linkedin.com/in "IIIT Lucknow" "{company_name}"')
    url = f'https://html.duckduckgo.com/html/?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []
    try:
        with httpx.Client(headers=headers, follow_redirects=True) as client:
            resp = client.get(url, timeout=10.0)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for a in soup.find_all('a', class_='result__snippet'):
                    if len(results) >= limit:
                        break
                    text = a.text
                    name = 'Alumni'
                    if 'View ' in text and "'s profile" in text:
                        name = text.split('View ')[1].split("'s profile")[0]
                    href = a.get('href', '')
                    if 'uddg=' in href:
                        parsed = urllib.parse.urlparse(href)
                        qs = urllib.parse.parse_qs(parsed.query)
                        if 'uddg' in qs:
                            real_url = qs['uddg'][0]
                            if 'linkedin.com/in/' in real_url:
                                results.append((name, real_url))
    except Exception:
        pass
    return results

