import json
import os
from datetime import datetime
import re

FORUM_FILE = "forum_data.json"

def sanitize_input(text, max_length=500):
    if not text or not isinstance(text, str):
        return ""
    text = text.strip()[:max_length]
    text = re.sub(r'<[^>]+>', '', text)
    return text

def load_forum_data():
    if os.path.exists(FORUM_FILE):
        try:
            with open(FORUM_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    return []

def save_forum_data(data):
    try:
        with open(FORUM_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

def add_forum_post(name, topic, message):
    name = sanitize_input(name, 100)
    topic = sanitize_input(topic, 200)
    message = sanitize_input(message, 1000)
    
    if not name or not topic or not message:
        return False
    
    if len(name) < 2 or len(topic) < 5 or len(message) < 10:
        return False
    
    posts = load_forum_data()
    
    new_post = {
        "id": len(posts) + 1,
        "name": name,
        "topic": topic,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "replies": []
    }
    
    posts.insert(0, new_post)
    
    if len(posts) > 100:
        posts = posts[:100]
    
    return save_forum_data(posts)

def get_forum_posts(limit=10):
    posts = load_forum_data()
    return posts[:limit]
