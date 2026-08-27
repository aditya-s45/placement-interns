import os
import urllib.parse
import httpx

def notify_new_jobs(store_data: dict, new_ids: list[str]) -> None:
    api_key = os.environ.get('CALLMEBOT_APIKEY')
    phone = os.environ.get('WHATSAPP_PHONE')
    
    if not api_key or not phone:
        print('  [WhatsApp] Missing CALLMEBOT_APIKEY or WHATSAPP_PHONE. Skipping alerts.')
        return
        
    if not new_ids:
        return
        
    new_jobs = [store_data[jid] for jid in new_ids if jid in store_data]
    if not new_jobs:
        return
        
    print(f'  [WhatsApp] Sending alert for {len(new_jobs)} new roles...')
    
    lines = ['🚨 *New Internships Found!* 🚨', '']
    for j in new_jobs:
        company = j.get('company', 'Unknown')
        title = j.get('title', 'Role')
        loc = j.get('location', 'N/A')
        url = j.get('url', '')
        lines.append(f'🏢 *{company}*')
        lines.append(f'💼 {title}')
        lines.append(f'📍 {loc}')
        lines.append(f'🔗 {url}')
        lines.append('')
        
    lines.append('See all at: https://aditya-s45.github.io/placement-interns/')
    
    text = '
'.join(lines)
    encoded_text = urllib.parse.quote(text)
    url = f'https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_text}&apikey={api_key}'
    
    try:
        resp = httpx.get(url, timeout=20.0)
        resp.raise_for_status()
        print('  [WhatsApp] Alert sent successfully!')
    except Exception as e:
        print(f'  [WhatsApp] Failed to send alert: {e}')
