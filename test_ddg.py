import urllib.parse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

query = urllib.parse.quote('site:linkedin.com/in "IIIT Lucknow" "Google"')
url = f'https://html.duckduckgo.com/html/?q={query}'

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        page.goto(url)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    snippets = soup.find_all('a', class_='result__snippet')
    print(f'Found {len(snippets)} snippets')
    if not snippets:
        print('No snippets found. Title:', soup.title.string if soup.title else 'No title')
except Exception as e:
    print(e)
