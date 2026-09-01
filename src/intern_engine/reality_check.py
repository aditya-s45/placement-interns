import os
import json
import httpx
from playwright.sync_api import sync_playwright

from . import paths
from . import llm

def evaluate_fit(job_url: str, resume_text: str = None) -> dict | None:
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        return None
        
    if not resume_text:
        resume_path = os.path.join(paths.ROOT, 'resume.txt')
        if not os.path.exists(resume_path):
            return None
        with open(resume_path, 'r', encoding='utf-8') as f:
            resume_text = f.read().strip()
        
    if len(resume_text) < 100 or 'PASTE YOUR RESUME' in resume_text:
        return None
        
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page.goto(job_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000) # Give React/Angular a moment to mount the DOM
            jd_text = page.inner_text("body")[:15000]
            browser.close()
    except Exception as e:
        print(f"  [RealityCheck] Playwright error: {e}")
        return None
        
    prompt = (
        "You are a brutal, highly critical technical recruiter. "
        "I will provide a job description and a candidate's resume. "
        "Compare them and return a JSON object with strictly these keys:\n"
        "'score': An integer from 0 to 100 representing how good of a match they are.\n"
        "'critique': A single brutally honest sentence explaining their biggest missing skill or why they might get rejected.\n"
        "'missing_keywords': A JSON list of strings representing the hard technical skills, tools, or languages (e.g. 'React', 'Kubernetes', 'C++') that are explicitly required in the job description but are completely missing from the candidate's resume. Keep the list concise (max 5 keywords).\n"
        "'tailored_bullets': If the score is 75 or higher, provide a list of 3 strings. Each string should be an existing bullet point from the resume rewritten to perfectly highlight skills relevant to this specific job description. If the score is below 75, omit this key.\n"
        "Do not include any markdown formatting, only valid JSON."
    )
    
    try:
        with httpx.Client() as client:
            resp = client.post(
                'https://openrouter.ai/api/v1/chat/completions',
                json={
                    'model': 'openrouter/free',
                    'messages': [
                        {'role': 'system', 'content': prompt},
                        {'role': 'user', 'content': f'JOB DESCRIPTION:\n{jd_text}\n\nRESUME:\n{resume_text}'}
                    ]
                },
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=30.0
            )
            data = resp.json()
            content = data['choices'][0]['message']['content'].strip()
            if content.startswith('```'):
                import re
                content = re.sub(r'^```(?:json)?\s*', '', content)
                content = re.sub(r'\s*```$', '', content)
            return json.loads(content)
    except Exception as e:
        print(f'  [RealityCheck] Error: {e}')
        return None
