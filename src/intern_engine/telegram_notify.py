import os
import httpx
from . import referrals

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
    
    lines = ['?? *New Internships Found!* ??', '']
    for j in new_jobs:
        company = j.get('company', 'Unknown')
        title = j.get('title', 'Role')
        loc = j.get('location', 'N/A')
        url = j.get('url', '')
        lines.append(f'?? *{company}*')
        lines.append(f'?? {title}')
        lines.append(f'?? {loc}')
        lines.append(f'?? [Apply Here]({url})')
        
        # The Inside Man feature
        alumni = referrals.find_alumni(company)
        if alumni:
            lines.append('')
            lines.append(f'?? *IIIT Lucknow Alumni at {company}:*')
            for name, link in alumni:
                lines.append(f'• [{name}]({link})')
            lines.append('')
            lines.append(f'_"Hi {{Name}}, I saw your journey from IIIT Lucknow to {company} and was really inspired. I am currently applying for their internship and would love to ask you 2 quick questions about your experience if you have a moment!"_')
        lines.append('')
        lines.append('???????????????')
        lines.append('')
        
    lines.append('See all at: https://aditya-s45.github.io/placement-interns/')
    text = '
'.join(lines)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        resp = httpx.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown', 'disable_web_page_preview': True}, timeout=20.0)
        resp.raise_for_status()
        print('  [Telegram] Alert sent successfully!')
    except Exception as e:
        print(f'  [Telegram] Failed to send alert: {e}')

