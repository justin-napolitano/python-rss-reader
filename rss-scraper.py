import feedparser
from datetime import datetime
import requests
import json
import argparse
import os
from gcputils.GoogleCloudLogging import GoogleCloudLogging
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news_feed(feed_url="https://jnapolitano.com/index.xml"):
    try:
        NewsFeed = feedparser.parse(feed_url)
        return NewsFeed
    except Exception as e:
        logging.error(f"An error occurred while fetching the news feed: {e}")
        return None


def format_datetime(date_str, date_format="%a, %d %b %Y %H:%M:%S %z"):
    try:
        dt = datetime.strptime(date_str, date_format)
        formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
        return formatted_date
    except Exception as e:
        logging.error(f"An error occurred while formatting date: {e}")
        return None


def update_database_feed(entry, base_url):
    try:
        print("updating database feed")
        url = f"{base_url}/update/feed"
        headers = {'Content-Type': 'application/json'}
        formatted_pub_date = format_datetime(entry.get('published'))
        # print("entry"  f"{entry}")
        # Example usage

        data = {
            "title": entry.get('title'),
            "link": clean_url(entry.get('link')),
            "pubDate": formatted_pub_date,
            "guid": clean_url(entry.get('id')),
            "description": entry.get('summary')
        }
        # print("data:" f"{data}")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            logging.info(f"Successfully added entry: {data['title']}")
            logging.info(response.json)
        elif response.status_code == 200:
            logging.info(f"Entry updated or no update needed for: {data['title']}")
            logging.info(response.json)
        else:
            logging.error(f"Failed to update database for entry: {data['title']}, Status Code: {response.status_code}, Message: {response.text}")
    except Exception as e:
        # print(f"error {e}")
        logging.error(f"An error occurred while updating the database: {e}")


def update_database_build(entry, base_url):
    try:
        url = f"{base_url}/update/builds"
        headers = {'Content-Type': 'application/json'}
        formatted_last_build_date = format_datetime(entry.get('lastBuildDate'))
        data = {
            "title": entry.get('title'),
            "link": entry.get('link'),
            "description": entry.get('description'),
            "generator": entry.get('generator'),
            "language": entry.get('language'),
            "copyright": entry.get('copyright'),
            "lastBuildDate": formatted_last_build_date,
            "atom_link_href": entry.get('atom_link_href'),
            "atom_link_rel": entry.get('atom_link_rel'),
            "atom_link_type": entry.get('atom_link_type')
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            logging.info(f"Successfully added build: {data['title']}")
        elif response.status_code == 200:
            logging.info(f"Build updated or no update needed for: {data['title']}")
        else:
            logging.error(f"Failed to update database for build: {data['title']}, Status Code: {response.status_code}, Message: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred while updating the database: {e}")


def clean_url(url,lang_code = "en"):
     # Find the position of the first occurrence of "jnapolitano.com"
    first_occurrence = url.find("jnapolitano.com")
    # Find the position of the second occurrence of "jnapolitano.com"
    second_occurrence = url.find("jnapolitano.com", first_occurrence + len("jnapolitano.com"))
    
    # If the second occurrence is found, remove it and the slash following it
    if second_occurrence != -1:
        url = url[:second_occurrence] + url[second_occurrence + len("jnapolitano.com") + 1:]

    # Add the language code (e.g., /en) after the domain
    first_occurrence_end = first_occurrence + len("jnapolitano.com")
    clean_url = url[:first_occurrence_end] + f"/{lang_code}" + url[first_occurrence_end:]

    return clean_url



def process_feed(base_url):
    try:
        NewsFeed = get_news_feed()
        
        if not NewsFeed:
            logging.error("Failed to retrieve news feed.")
            return

        for entry in NewsFeed.entries:
            # Unpacking dictionary keys to variables
            title = entry.get('title')
            title_detail = entry.get('title_detail')
            links = entry.get('links')
            link = entry.get('link')
            published = entry.get('published')
            published_parsed = entry.get('published_parsed')
            entry_id = entry.get('id')
            guidislink = entry.get('guidislink')
            summary = entry.get('summary')
            summary_detail = entry.get('summary_detail')
            # description = entry.get('description')
            # generator = entry.get('generator')
            # language = entry.get('language')
            # copyright = entry.get('copyright')
            # last_build_date = entry.get('lastBuildDate')
            # atom_link_href = entry.get('atom_link_href')
            # atom_link_rel = entry.get('atom_link_rel')
            # atom_link_type = entry.get('atom_link_type')

            # Logging for debugging
            logging.info(f"Title: {title}")
            logging.info(f"Title Detail: {title_detail}")
            logging.info(f"Links: {links}")
            logging.info(f"Link: {link}")
            logging.info(f"Published: {published}")
            logging.info(f"Published Parsed: {published_parsed}")
            logging.info(f"ID: {entry_id}")
            logging.info(f"GUID is Link: {guidislink}")
            logging.info(f"Summary: {summary}")
            logging.info(f"Summary Detail: {summary_detail}")

            if published:
                # print("calling update_database_feed")
                logging.info(f"New entry found: {title}" )
                update_database_feed(entry, base_url)

    except Exception as e:
        logging.error(f"An error occurred during the process: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process RSS feed updates.')
    parser.add_argument('--url', type=str, default="https://rss-updater-pkpovjepjq-wl.a.run.app",
                        help='Base URL for the API endpoint')
    parser.add_argument('--local', action='store_true', help='Use local credentials for Google Cloud Logging')
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()
    # Setup Google Cloud Logging
    project_id = os.environ.get("PROJECT_NAME")
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") if args.local else None
    # print(project_id)
    # gcl = GoogleCloudLogging(project_id, credentials_path)
    # gcl.setup_logging()

    # Run the feed processing with the provided URL or default
    process_feed(args.url)
