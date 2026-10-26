import os
import json
import httpx
from bs4 import BeautifulSoup

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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        with httpx.Client(timeout=15.0, follow_redirects=True) as client:
            resp = client.get(job_url, headers=headers)
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, 'html.parser')
            for tag in soup(["script", "style", "noscript", "svg"]):
                tag.extract()
            jd_text = soup.get_text(separator=' ')[:15000]
    except Exception as e:
        print(f"  [RealityCheck] Fetch error: {e}")
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
            resp.raise_for_status()
            data = resp.json()
            raw_content = data['choices'][0]['message']['content']
            
            # Robust JSON extraction
            cleaned_content = raw_content.strip()
            if cleaned_content.startswith('```'):
                lines = cleaned_content.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                cleaned_content = '\n'.join(lines).strip()
                
            return json.loads(cleaned_content)
    except Exception as e:
        print(f"  [RealityCheck] LLM evaluation error: {e}")
        return None
