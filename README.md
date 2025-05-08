# Crypto News Collector

**A real-time tool for collecting, storing, and archiving ALL unique crypto news from CryptoPanic API. News are saved in daily JSON files and automatically uploaded to Google Drive at each UTC midnight.**

---

## Features

- Collects all available news (no filters) from CryptoPanic free API.
- Stores each day’s unique news as a single JSON file (`YYYY-MM-DD.json`).
- At 00:00 UTC, uploads the file to a Google Drive folder and starts a new JSON for the new day.
- No duplicates – only new news items (by `id`) are added for each day.
- Full raw JSON from API is preserved.
- Minimal dependencies and one-file run.

---

## Project Structure

```
.env
.gitinore
collector.py
gdrive_credentials.json
requirements.txt
2025-05-08.json   # (Example)
```

---

## Installation

1. **Clone the repository and enter the directory:**
   ```bash
   git clone https://github.com/Pfauberg/crypto-news-collector.git
   cd crypto-news-collector
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Setup
### `.env` example
```
CRYPTOPANIC_TOKEN=your_cryptopanic_api_token
GDRIVE_FOLDER_ID=your_google_drive_folder_id
GDRIVE_CREDS_PATH=gdrive_credentials.json
```
- **CRYPTOPANIC_TOKEN** — get it from [cryptopanic.com/developers/api](https://cryptopanic.com/developers/api/)
- **GDRIVE_FOLDER_ID** — ID of your Google Drive destination folder  
- **GDRIVE_CREDS_PATH** — path to your Google service account credentials JSON

**Don’t forget to share your target GDrive folder with your service account email!**

For more general information on Google service accounts, see  
- [Google Cloud: Service Account Overview](https://cloud.google.com/iam/docs/service-account-overview)

--- 

## Usage

Just run:
```bash
python collector.py
```
---

## Output

- **One JSON file per UTC day**, e.g. `2025-05-08.json` (removed locally after uploading to GDrive).

---

## Notes

- Only latest news from CryptoPanic’s free API are collected (past history is not available on free plans).
- Make sure the process runs 24/7 for continuous coverage.
- Use the GDrive JSON dump in analytics, trading bots, research, news archiving, or resale.
