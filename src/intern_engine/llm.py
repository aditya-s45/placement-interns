import json
import os
import re
from typing import Any

from .net import Net

def _clean_html(html: str) -> str:
    """Strip head, styles, scripts, and SVG to reduce token count."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "svg", "path", "head", "noscript", "meta", "link", "iframe"]):
            tag.decompose()
        # Collapse whitespace
        text = soup.get_text(separator=" ")
        return re.sub(r'\s+', ' ', text).strip()
    except ImportError:
        # Fallback if bs4 is not available
        text = re.sub(r'<script.*?</script>', '', html, flags=re.IGNORECASE|re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.IGNORECASE|re.DOTALL)
        text = re.sub(r'<svg.*?</svg>', '', text, flags=re.IGNORECASE|re.DOTALL)
        text = re.sub(r'<.*?>', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()

async def extract_jobs_from_html(html: str, company_name: str, base_url: str, net: Net) -> list[dict[str, Any]]:
    """Use OpenRouter to extract job listings from HTML text."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print(f"  [LLM] OPENROUTER_API_KEY not set. Skipping LLM extraction for {company_name}.")
        return []

    cleaned_text = _clean_html(html)
    # Truncate text to a reasonable length to avoid exceeding context window (e.g. 50k chars)
    cleaned_text = cleaned_text[:50000]

    system_prompt = (
        "You are an API that extracts job postings from raw text of a career page. "
        "Return a JSON array of objects, where each object has these fields: "
        "'title' (string), 'location' (string, or '—' if unspecified), 'url' (absolute URL, string). "
        "If a URL is relative, prepend the base_url provided. "
        "Do not include any explanation or markdown wrapping around the JSON array, just output the raw JSON."
    )
    
    user_prompt = (
        f"Company: {company_name}\n"
        f"Base URL: {base_url}\n\n"
        f"Extract the jobs from this career page text:\n\n{cleaned_text}"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/10vulture1005/interns-work", 
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        resp = await net.client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30.0
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        
        # Clean up possible markdown code blocks if the model ignored instructions
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
            
        parsed = json.loads(content)
        if isinstance(parsed, dict) and "jobs" in parsed:
            return parsed["jobs"]
        if isinstance(parsed, list):
            return parsed
        return []
    except Exception as e:
        print(f"  [LLM] Failed to extract jobs for {company_name}: {e}")
        return []
