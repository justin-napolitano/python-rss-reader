---
slug: github-python-rss-reader-note-technical-overview
id: github-python-rss-reader-note-technical-overview
title: Python RSS Reader
repo: justin-napolitano/python-rss-reader
githubUrl: https://github.com/justin-napolitano/python-rss-reader
generatedAt: '2025-11-24T18:44:07.063Z'
source: github-auto
summary: >-
  This repo is a Python tool for parsing RSS feeds. It’s designed to automate
  Hugo blog updates to social media and other platforms. Key components include:
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: note
entryLayout: note
showInProjects: false
showInNotes: true
showInWriting: false
showInLogs: false
---

This repo is a Python tool for parsing RSS feeds. It’s designed to automate Hugo blog updates to social media and other platforms. Key components include:

- **RSS Parsing:** Uses `feedparser` to handle feed data.
- **Google Cloud Integration:** Works with BigQuery, Cloud Storage, and Cloud Logging.
- **Docker Support:** Easily deploy with Docker and Google Cloud Build.

## Quick Start

1. Clone the repo:
    ```bash
    git clone https://github.com/justin-napolitano/python-rss-reader.git
    cd python-rss-reader
    ```

2. (Optional) Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the scraper:
    ```bash
    python rss-scraper.py
    ```

### Gotchas

- Don't forget to add your Google Cloud credentials in `secret.json` or set `GOOGLE_APPLICATION_CREDENTIALS`.
