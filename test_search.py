import urllib.parse
import httpx
from bs4 import BeautifulSoup
import asyncio

async def test():
    query = urllib.parse.quote('site:linkedin.com/in "IIIT Lucknow" "Google"')
    url = f'https://html.duckduckgo.com/html/?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url, timeout=10.0)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for a in soup.find_all('a', class_='result__snippet'):
            print(a.text)
        for a in soup.find_all('a', class_='result__url'):
            print(a.get('href'))

asyncio.run(test())
