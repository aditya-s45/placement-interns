import urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def find_alumni(company_name: str, college: str = 'IIIT Lucknow', limit: int = 2) -> list:
    query = urllib.parse.quote(f'site:linkedin.com/in "{college}" "{company_name}"')
    url = f'https://lite.duckduckgo.com/lite/'
    results = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.fill("input[name='q']", f'site:linkedin.com/in "{college}" "{company_name}"')
            page.click("input[type='submit']")
            page.wait_for_timeout(2000)
            html = page.content()
            browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', class_='result-url'):
                if len(results) >= limit:
                    break
                href = a.get('href', '')
                if 'linkedin.com/in/' in href:
                    # Extract name from the previous row or just use Alumni
                    tr = a.find_parent('tr')
                    name = 'Alumni'
                    if tr and tr.previous_sibling:
                        prev_tr = tr.previous_sibling
                        if prev_tr.name == 'tr':
                            title_a = prev_tr.find('a', class_='result-snippet')
                            if title_a:
                                text = title_a.text
                                if ' - ' in text:
                                    name = text.split(' - ')[0]
                    results.append((name, href))
    except Exception as e:
        print(f"  [Referrals] Playwright error: {e}")
        
    return results
