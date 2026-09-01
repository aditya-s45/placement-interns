import os
import httpx
from . import referrals
from . import reality_check
from . import telegram_bot

def notify_new_jobs(store_data: dict, new_ids: list[str]) -> None:
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print('  [Telegram] Missing TELEGRAM_BOT_TOKEN. Skipping alerts.')
        return
    if not new_ids:
        return
    new_jobs = [store_data[jid] for jid in new_ids if jid in store_data]
    if not new_jobs:
        return
    
    users = telegram_bot.load_users()
    
    # Fallback to single user setup if database is empty
    if not users:
        legacy_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        if legacy_chat_id:
            users[legacy_chat_id] = {'first_name': 'Admin', 'subscribed': True, 'resume_text': None}
        else:
            print('  [Telegram] No users subscribed and no TELEGRAM_CHAT_ID fallback.')
            return

    print(f'  [Telegram] Broadcasting {len(new_jobs)} new roles to {len(users)} users...')
    
    with httpx.Client(timeout=20.0) as client:
        for chat_id, user_data in users.items():
            if not user_data.get('subscribed'):
                continue
                
            user_name = user_data.get('first_name', 'User')
            user_resume = user_data.get('resume_text')
            
            lines = [f'🚨 *New Internships Found, {user_name}!* 🚨', '']
            for j in new_jobs:
                company = j.get('company', 'Unknown')
                title = j.get('title', 'Role')
                loc = j.get('location', 'N/A')
                url = j.get('url', '')
                lines.append(f'🏢 *{company}*')
                lines.append(f'💼 {title}')
                lines.append(f'📍 {loc}')
                lines.append(f'🔗 [Apply Here]({url})')
                
                print(f'  [Telegram] Running reality check for {company} (User: {user_name})...')
                fit = reality_check.evaluate_fit(url, user_resume)
                if fit:
                    lines.append('')
                    lines.append('🤖 *Brutal Reality Check*')
                    score = fit.get('score', 0)
                    indicator = '🟢' if score >= 80 else '🟡' if score >= 50 else '🔴'
                    lines.append(f'Score: {score}% Match {indicator}')
                    lines.append(f'Critique: {fit.get("critique", "")}')
                    
                    missing = fit.get('missing_keywords', [])
                    if missing and isinstance(missing, list):
                        lines.append(f'Missing Keywords: [{", ".join(missing)}]')
                    
                    tailored = fit.get('tailored_bullets')
                    if tailored and isinstance(tailored, list):
                        lines.append('')
                        lines.append('✨ *Auto-Tailored Resume Bullets for this Role:*')
                        for bullet in tailored:
                            lines.append(f'• {bullet}')
                    
                alumni = referrals.find_alumni(company)
                if alumni:
                    lines.append('')
                    lines.append(f'🤝 *IIIT Lucknow Alumni at {company}:*')
                    for name, link in alumni:
                        lines.append(f'• [{name}]({link})')
                    lines.append('')
                    lines.append(f'_"Hi {{Name}}, I saw your journey from IIIT Lucknow to {company} and was really inspired. I am currently applying for their internship and would love to ask you 2 quick questions about your experience if you have a moment!"_')
                lines.append('')
                lines.append('━━━━━━━━━━━━━━━')
                lines.append('')
                
            lines.append('See all at: https://aditya-s45.github.io/placement-interns/')
            text = '\n'.join(lines)
            tg_url = f'https://api.telegram.org/bot{token}/sendMessage'
            try:
                resp = client.post(tg_url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown', 'disable_web_page_preview': True})
                resp.raise_for_status()
            except Exception as e:
                print(f'  [Telegram] Failed to send alert to {user_name} ({chat_id}): {e}')
