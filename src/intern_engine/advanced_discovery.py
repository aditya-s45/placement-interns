import os
import re
import json
import urllib.parse
import httpx
from bs4 import BeautifulSoup

from . import llm

_KNOWN_DOMAINS = {
    'greenhouse.io': 'greenhouse',
    'lever.co': 'lever',
    'ashbyhq.com': 'ashby',
    'smartrecruiters.com': 'smartrecruiters',
    'workable.com': 'workable',
    'myworkdayjobs.com': 'workday',
    'icims.com': 'icims',
    'successfactors.com': 'successfactors',
}

async def search_duckduckgo(company_name: str, client: httpx.AsyncClient) -> str | None:
    query = urllib.parse.quote(f'{company_name} careers internships')
    url = f'https://html.duckduckgo.com/html/?q={query}'
    try:
        resp = await client.get(url, timeout=10.0)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for a in soup.find_all('a', class_='result__url'):
                href = a.get('href', '')
                if 'duckduckgo' not in href:
                    return href
            for a in soup.find_all('a'):
                href = a.get('href', '')
                if href.startswith('http') and 'duckduckgo' not in href and 'yahoo' not in href:
                    if 'career' in href.lower() or 'job' in href.lower():
                        return href
    except Exception:
        pass
    return None

async def resolve_untracked(untracked_names: list[str]) -> list[dict]:
    if not untracked_names:
        return []
    resolved = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        for name in untracked_names:
            print(f'  [Tier 2] Searching for careers page for: {name}')
            careers_url = await search_duckduckgo(name, client)
            if not careers_url:
                print('    -> Could not find careers page via search.')
                continue
            print(f'    -> Found: {careers_url}')
            try:
                resp = await client.get(careers_url, timeout=15.0)
                html = resp.text
            except Exception as e:
                print(f'    -> Failed to load careers page: {e}')
                continue
            soup = BeautifulSoup(html, 'html.parser')
            found_ats = None
            found_slug = None
            for a in soup.find_all('a', href=True):
                href = a['href']
                for domain, ats_name in _KNOWN_DOMAINS.items():
                    if domain in href:
                        parts = [p for p in href.split('/') if p]
                        if len(parts) >= 3:
                            found_ats = ats_name
                            found_slug = parts[-1].split('?')[0]
                            break
                if found_ats:
                    break
            if found_ats and found_slug:
                print(f'    -> [Tier 2] Found ATS link! {found_ats} (slug: {found_slug})')
                resolved.append({'name': name, 'slug': found_slug, 'ats': found_ats})
                continue
            api_key = os.environ.get('OPENROUTER_API_KEY')
            if not api_key:
                print('    -> No known ATS link found. OPENROUTER_API_KEY missing, skipping Tier 3.')
                continue
            print('    -> No known ATS link found. Running Tier 3 (LLM CSS extraction)...')
            cleaned_html = llm._clean_html(html)[:50000]
            prompt = ('You are an expert web scraper. I will give you the HTML of a careers page. '
                      'Find the CSS selector that uniquely targets the container for each individual job posting in the list. '
                      'Return ONLY a JSON object like this: {"css_hint": ".job-item"} or {"css_hint": "li.posting"}. '
                      'Do not include markdown or explanations.')
            try:
                resp = await client.post('https://openrouter.ai/api/v1/chat/completions', json={'model': 'openrouter/free', 'messages': [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': cleaned_html}]}, headers={'Authorization': f'Bearer {api_key}'}, timeout=40.0)
                data = resp.json()
                content = data['choices'][0]['message']['content'].strip()
                if content.startswith('```'):
                    content = re.sub(r'^```(?:json)?\s*', '', content)
                    content = re.sub(r'\s*```$', '', content)
                parsed = json.loads(content)
                css_hint = parsed.get('css_hint')
                if css_hint:
                    print(f'    -> [Tier 3] Extracted custom CSS selector: {css_hint}')
                    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
                    resolved.append({'name': name, 'slug': slug, 'ats': 'custom', 'url': careers_url, 'css_hint': css_hint})
            except Exception as e:
                print(f'    -> [Tier 3] Failed to extract CSS hint: {e}')
    return resolved
