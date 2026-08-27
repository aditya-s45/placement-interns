import urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def find_alumni(company_name: str, college: str = 'IIIT Lucknow', limit: int = 2) -> list:
    query = urllib.parse.quote(f'site:linkedin.com/in "{college}" "{company_name}"')
    url = f'https://html.duckduckgo.com/html/?q={query}'
    results = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            html = page.content()
            browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
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
    except Exception as e:
        print(f"  [Referrals] Playwright error: {e}")
        
    return results
