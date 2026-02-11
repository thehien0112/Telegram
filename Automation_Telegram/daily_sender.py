import os
import json
import random
import requests
import re
from datetime import datetime

# Load Config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')

# Default config
config = {
    "content_dir": "../",
    "db_file": "sent_log.json"
}

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config.update(json.load(f))

CONTENT_DIR_PLAN_B = os.path.join(SCRIPT_DIR, config.get('content_dir', '../'))
CONTENT_DIR_NB = os.path.join(SCRIPT_DIR, 'NotebookLM_Queue')
DB_FILE = os.path.join(SCRIPT_DIR, config.get('db_file', 'sent_log.json'))

# Priority: Env Vars (GitHub Actions) > Config File (Local)
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN') or config.get('bot_token')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or config.get('chat_id')

if not BOT_TOKEN or not CHAT_ID:
    print("Error: Missing Bot Token or Chat ID.")
    exit(1)

def load_sent_log():
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except:
        return []

def save_sent_log(log):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=4)

def get_next_content(sent_log):
    # Priority 1: Check NotebookLM Queue
    if os.path.exists(CONTENT_DIR_NB):
        for f in sorted(os.listdir(CONTENT_DIR_NB)):
            if f.endswith('.md') and f not in sent_log:
                return os.path.join(CONTENT_DIR_NB, f), f

    # Priority 2: Check Plan B Content
    if os.path.exists(CONTENT_DIR_PLAN_B):
        plan_b_files = []
        for f in os.listdir(CONTENT_DIR_PLAN_B):
            if f.endswith('.md') and 'plan' not in f.lower() and 'roadmap' not in f.lower() and 'deploy' not in f.lower():
                if f not in sent_log:
                    plan_b_files.append(f)
        
        # Sort Plan B files (Simple alphabetical is fine for now, or random)
        if plan_b_files:
            plan_b_files.sort() 
            return os.path.join(CONTENT_DIR_PLAN_B, plan_b_files[0]), plan_b_files[0]
            
    return None, None

def parse_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    title = os.path.basename(filepath)
    body_lines = []
    
    # Extract Title
    for line in lines:
        if line.strip().startswith('# '):
            title = line.strip().replace('# ', '').replace('*', '')
            break
            
    # Clean up body
    for line in lines:
        if line.strip().startswith('# '): continue
        if line.strip().startswith('**Format:**'): continue
        if line.strip().startswith('**Chủ đề:**'): continue
        
        # Replace image placeholder
        if '**(' in line and ')**' in line:
            line = re.sub(r'\*\*\((.*?)\)\*\*', r'📸 *[Minh họa: \1]*', line)
            
        body_lines.append(line)
        
    body = '\n'.join(body_lines).strip()
    return title, body

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    print(f"[{datetime.now()}] Starting Daily Sender...")
    
    sent_log = load_sent_log()
    
    filepath, filename = get_next_content(sent_log)
    
    if not filepath:
        print("No new content available to send.")
        return

    print(f"Selected: {filename}")
    
    title, body = parse_content(filepath)
    
    # Sanitize Markdown for Telegram V1
    # 1. Bold: Convert **text** to *text*
    body = re.sub(r'\*\*(.*?)\*\*', r'*\1*', body)
    title = re.sub(r'\*\*(.*?)\*\*', r'*\1*', title)
    
    # 2. Italic: Convert *text* to _text_ (if not already handled, but careful with bullets)
    # Actually, keep *text* as bold for Telegram V1 is *bold*, _italic_. 
    # Standard MD: **bold**, *italic*.
    # So ** -> * (Bold), * -> _ (Italic) is complex if nested.
    # Simple fix: Just handle ** -> * for Bold. Leave _ for italic.
    
    # 3. Bullets: Convert '* ' at start of line to '• ' to avoid unclosed bold
    body = re.sub(r'^\* ', '• ', body, flags=re.MULTILINE)
    
    # 4. Headers: Convert ## Title to *Title*
    body = re.sub(r'^#+ (.*?)$', r'*\1*', body, flags=re.MULTILINE)

    # Format Message
    # Check if NB generated to change footer
    # Use single _ for italic footer, not double __
    source_text = "Mẹ Ba Vì (NotebookLM)" if "NB" in filename else "Mẹ Ba Vì (Plan B)"
    message = f"🌿 *{title}*\n\n{body}\n\n_{source_text}_"
    
    # Send
    try:
        resp = send_telegram_message(message)
        if resp.get('ok'):
            print("Message sent successfully!")
            sent_log.append(filename)
            save_sent_log(sent_log)
        else:
            print(f"Failed to send: {resp}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    main()
