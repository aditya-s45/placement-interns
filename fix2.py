import codecs
content = '''import os
import httpx
from . import referrals
from . import reality_check

def notify_new_jobs(store_data: dict, new_ids: list[str]) -> None:
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        print('  [Telegram] Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID. Skipping alerts.')
        return
    if not new_ids:
        return
    new_jobs = [store_data[jid] for jid in new_ids if jid in store_data]
    if not new_jobs:
        return
    print(f'  [Telegram] Sending alert for {len(new_jobs)} new roles...')
    
    lines = ['[ALERT] *New Internships Found!*', '']
    for j in new_jobs:
        company = j.get('company', 'Unknown')
        title = j.get('title', 'Role')
        loc = j.get('location', 'N/A')
        url = j.get('url', '')
        lines.append(f'*Company:* {company}')
        lines.append(f'*Role:* {title}')
        lines.append(f'*Location:* {loc}')
        lines.append(f'[Apply Here]({url})')
        
        print(f'  [Telegram] Running reality check for {company}...')
        fit = reality_check.evaluate_fit(url)
        if fit:
            lines.append('')
            lines.append('[BOT] *Brutal Reality Check*')
            score = fit.get('score', 0)
            indicator = 'PASS' if score >= 80 else 'AVERAGE' if score >= 50 else 'FAIL'
            lines.append(f'Score: {score}% Match ({indicator})')
            lines.append(f'Critique: {fit.get("critique", "")}')
            
            missing = fit.get('missing_keywords', [])
            if missing and isinstance(missing, list):
                lines.append(f'Missing Keywords: [{ ", ".join(missing) }]')
            
            tailored = fit.get('tailored_bullets')
            if tailored and isinstance(tailored, list):
                lines.append('')
                lines.append('[AI] *Auto-Tailored Resume Bullets for this Role:*')
                for bullet in tailored:
                    lines.append(f'- {bullet}')
            
        alumni = referrals.find_alumni(company)
        if alumni:
            lines.append('')
            lines.append(f'[NETWORK] *IIIT Lucknow Alumni at {company}:*')
            for name, link in alumni:
                lines.append(f'- [{name}]({link})')
            lines.append('')
            lines.append(f'_"Hi {{Name}}, I saw your journey from IIIT Lucknow to {company} and was really inspired. I am currently applying for their internship and would love to ask you 2 quick questions about your experience if you have a moment!"_')
        lines.append('')
        lines.append('---------------')
        lines.append('')
        
    lines.append('See all at: https://aditya-s45.github.io/placement-interns/')
    text = '
'.join(lines)
    tg_url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        resp = httpx.post(tg_url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown', 'disable_web_page_preview': True}, timeout=20.0)
        resp.raise_for_status()
        print('  [Telegram] Alert sent successfully!')
    except Exception as e:
        print(f'  [Telegram] Failed to send alert: {e}')
'''
with codecs.open('src/intern_engine/telegram_notify.py', 'w', 'utf-8') as f:
    f.write(content)
