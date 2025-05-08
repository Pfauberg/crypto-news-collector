import os
import requests
import json
import time
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

load_dotenv('.env')
TOKEN = os.getenv("CRYPTOPANIC_TOKEN")
BASE_URL = "https://cryptopanic.com/api/v1/posts/"
LIMIT = 100
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID")
GDRIVE_CREDS_PATH = os.getenv("GDRIVE_CREDS_PATH")

def utc_date_string(dt=None):
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime('%Y-%m-%d')

def today_json_name():
    return f"{utc_date_string()}.json"

def tomorrow_utc_seconds():
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait = (tomorrow - now).total_seconds()
    return wait

def upload_to_gdrive(local_path, filename):
    creds = Credentials.from_service_account_file(GDRIVE_CREDS_PATH, scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': filename,
        'parents': [GDRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(local_path, mimetype='application/json')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def fetch_latest_news(seen_ids):
    params = {"auth_token": TOKEN, "limit": LIMIT}
    resp = requests.get(BASE_URL, params=params)
    if resp.status_code != 200:
        return []
    posts = resp.json().get("results", [])
    new_posts = []
    for post in posts:
        _id = post.get("id")
        if _id and _id not in seen_ids:
            new_posts.append(post)
            seen_ids.add(_id)
    return new_posts

if __name__ == "__main__":
    news_file = today_json_name()
    if os.path.exists(news_file):
        with open(news_file, encoding='utf-8') as f:
            news_data = json.load(f)
            seen_ids = set(news['id'] for news in news_data if 'id' in news)
    else:
        news_data = []
        seen_ids = set()

    while True:
        new_news = fetch_latest_news(seen_ids)
        if new_news:
            news_data.extend(new_news)
            with open(news_file, "w", encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
        seconds_left = tomorrow_utc_seconds()
        if seconds_left <= 60:  # less than a minute to midnight UTC!
            if news_data:
                upload_to_gdrive(news_file, news_file)
            if os.path.exists(news_file):
                os.remove(news_file)
            news_data = []
            seen_ids = set()
            news_file = today_json_name()
            time.sleep(90)
            continue
        time.sleep(300)