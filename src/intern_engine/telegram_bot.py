import os
import json
import httpx
from . import paths

USERS_FILE = os.path.join(paths.DATA_DIR, 'users.json')
STATE_FILE = os.path.join(paths.DATA_DIR, 'bot_state.json')

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'last_update_id': 0}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def send_msg(client, token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        client.post(url, json={'chat_id': chat_id, 'text': text})
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")

def poll():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Missing TELEGRAM_BOT_TOKEN")
        return

    users = load_users()
    state = load_state()
    offset = state.get('last_update_id', 0) + 1

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    with httpx.Client(timeout=10.0) as client:
        try:
            resp = client.post(url, json={'offset': offset, 'timeout': 5})
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Error fetching updates: {e}")
            return

        if not data.get('ok') or not data.get('result'):
            print("No new messages.")
            return

        for update in data['result']:
            update_id = update['update_id']
            state['last_update_id'] = max(state.get('last_update_id', 0), update_id)

            msg = update.get('message')
            if not msg or 'text' not in msg:
                continue

            chat_id = str(msg['chat']['id'])
            text = msg['text'].strip()
            first_name = msg['chat'].get('first_name', 'User')

            if text.startswith('/start') or text.startswith('/subscribe'):
                if chat_id not in users:
                    users[chat_id] = {
                        'first_name': first_name,
                        'resume_text': '',
                        'subscribed': True
                    }
                    send_msg(client, token, chat_id, f"Welcome to the IIIT Lucknow Job Bot, {first_name}! 🚀\n\nPlease reply by pasting the plain text of your resume here. This will be used by our AI to grade your fit for new internships.")
                else:
                    users[chat_id]['subscribed'] = True
                    send_msg(client, token, chat_id, "You are already subscribed! If you want to update your resume, just paste the new text.")
            
            elif text.startswith('/unsubscribe'):
                if chat_id in users:
                    users[chat_id]['subscribed'] = False
                    send_msg(client, token, chat_id, "You have been unsubscribed from job alerts.")
            
            elif len(text) > 200:
                # Assume it's a resume update
                if chat_id not in users:
                    users[chat_id] = {'first_name': first_name, 'subscribed': True}
                
                users[chat_id]['resume_text'] = text
                send_msg(client, token, chat_id, "✅ Resume successfully registered! You will now receive personalized AI reality checks for new job postings.")

        save_users(users)
        save_state(state)
        print(f"Processed {len(data['result'])} updates.")
