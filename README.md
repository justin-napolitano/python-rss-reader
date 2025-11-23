# python-rss-reader

A Python-based tool designed to parse and process RSS feeds, primarily aimed at automating the posting of Hugo blog updates to social media or other platforms. This project includes utilities for interacting with Google Cloud services and supports deployment via Docker and Google Cloud Build.

---

## Features

- Parses RSS feeds to extract and process new blog entries.
- Converts published dates to standardized formats for comparison and processing.
- Updates a backend service or database with new or updated feed entries via HTTP requests.
- Integrates with Google Cloud services including BigQuery, Cloud Storage, and Cloud Logging through reusable client utilities.
- Supports containerized deployment with Docker and automated builds using Google Cloud Build.

---

## Tech Stack

- Python 3
- feedparser (for RSS parsing)
- requests (for HTTP requests)
- Google Cloud SDKs (BigQuery, Storage, Logging)
- Docker
- Google Cloud Build

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Docker (optional, for containerized deployment)
- Google Cloud account and appropriate permissions

### Installation

1. Clone the repository:

```bash
git clone https://github.com/justin-napolitano/python-rss-reader.git
cd python-rss-reader
```

2. (Optional) Set up a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables and credentials:

- Place your Google Cloud service account JSON in `secret.json` or set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`.

- Configure any other required environment variables as needed.

### Running the RSS Scraper

```bash
python rss-scraper.py
```

This will parse the RSS feed (default: `https://jnapolitano.com/index.xml`) and attempt to update the backend service with new entries.

### Using Docker

Build the Docker image:

```bash
docker build -t python-rss-reader .
```

Run the container:

```bash
docker run --env GOOGLE_APPLICATION_CREDENTIALS=/path/to/secret.json -v /local/path/to/secret.json:/path/to/secret.json python-rss-reader
```

### Google Cloud Build

The `cloudbuild.yaml` file defines steps to build and push the Docker image to Google Container Registry. Uncomment and configure additional steps to deploy to Cloud Run or set up Cloud Scheduler jobs.

Run Cloud Build:

```bash
gcloud builds submit --config cloudbuild.yaml .
```

---

## Project Structure

```
python-rss-reader/
├── cloudbuild.yaml          # Google Cloud Build configuration
├── Dockerfile               # Docker image definition
├── gcputils/                # Google Cloud utility submodule
│   ├── BigQueryClient.py    # BigQuery client wrapper
│   ├── GCSClient.py         # Google Cloud Storage client wrapper
│   ├── GoogleCloudLogging.py# Cloud Logging client wrapper
│   ├── index.md             # Documentation
│   └── readme.md            # Documentation
├── images/                  # Image assets
├── index.md                 # Project notes and thoughts
├── last_run.txt             # Stores last run timestamp
├── readme.md                # Project notes and thoughts (similar to index.md)
├── requirements.txt         # Python dependencies
├── rss-scraper.py           # Main RSS parsing and update script
└── secret.json              # Google Cloud service account credentials (sensitive)
```

---

## Future Work / Roadmap

- Implement a dedicated API or batch processor for handling feed updates instead of a monolithic script.
- Add more robust error handling and retry mechanisms.
- Extend support for publishing parsed posts to various social media platforms.
- Enhance configuration management for cloud deployments.
- Add automated tests and CI/CD pipelines.
- Improve documentation and usage examples.

---

*Note: This README is based on available source files and inferred project goals. Some assumptions were made regarding deployment and usage.*