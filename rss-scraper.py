import feedparser
from datetime import datetime
import requests
import json
import argparse

def get_news_feed(feed_url="https://jnapolitano.com/index.xml"):
    try:
        NewsFeed = feedparser.parse(feed_url)
        return NewsFeed
    except Exception as e:
        print(f"An error occurred while fetching the news feed: {e}")
        return None


def format_datetime(date_str, date_format="%a, %d %b %Y %H:%M:%S %z"):
    try:
        dt = datetime.strptime(date_str, date_format)
        formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
        return formatted_date
    except Exception as e:
        print(f"An error occurred while formatting date: {e}")
        return None


def update_database_feed(entry, base_url):
    try:
        url = f"{base_url}/update/feed"
        headers = {'Content-Type': 'application/json'}
        formatted_pub_date = format_datetime(entry.get('published'))
        data = {
            "title": entry.get('title'),
            "link": entry.get('link'),
            "pubDate": formatted_pub_date,
            "guid": entry.get('id'),
            "description": entry.get('summary')
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            print(f"Successfully added entry: {data['title']}")
        elif response.status_code == 200:
            print(f"Entry updated or no update needed for: {data['title']}")
        else:
            print(f"Failed to update database for entry: {data['title']}, Status Code: {response.status_code}, Message: {response.text}")
    except Exception as e:
        print(f"An error occurred while updating the database: {e}")


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
            print(f"Successfully added build: {data['title']}")
        elif response.status_code == 200:
            print(f"Build updated or no update needed for: {data['title']}")
        else:
            print(f"Failed to update database for build: {data['title']}, Status Code: {response.status_code}, Message: {response.text}")
    except Exception as e:
        print(f"An error occurred while updating the database: {e}")


def process_feed(base_url):
    try:
        NewsFeed = get_news_feed()
        
        if not NewsFeed:
            print("Failed to retrieve news feed.")
            return

        for entry in NewsFeed.entries:
            # Unpacking dictionary keys to variables
            title = entry.get('title')
            # title_detail = entry.get('title_detail')
            # links = entry.get('links')
            # link = entry.get('link')
            published = entry.get('published')
            # published_parsed = entry.get('published_parsed')
            # entry_id = entry.get('id')
            # guidislink = entry.get('guidislink')
            # summary = entry.get('summary')
            # summary_detail = entry.get('summary_detail')
            # description = entry.get('description')
            # generator = entry.get('generator')
            # language = entry.get('language')
            # copyright = entry.get('copyright')
            # last_build_date = entry.get('lastBuildDate')
            # atom_link_href = entry.get('atom_link_href')
            # atom_link_rel = entry.get('atom_link_rel')
            # atom_link_type = entry.get('atom_link_type')

            # # Logging for debugging
            # print(f"Title: {title}")
            # print(f"Title Detail: {title_detail}")
            # print(f"Links: {links}")
            # print(f"Link: {link}")
            # print(f"Published: {published}")
            # print(f"Published Parsed: {published_parsed}")
            # print(f"ID: {entry_id}")
            # print(f"GUID is Link: {guidislink}")
            # print(f"Summary: {summary}")
            # print(f"Summary Detail: {summary_detail}")

            if published:
                print("New entry found:", title)
                update_database_feed(entry, base_url)

            # if last_build_date:
            #     print("New build found:", title)
            #     update_database_build(entry, base_url)

    except Exception as e:
        print(f"An error occurred during the process: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process RSS feed updates.')
    parser.add_argument('--url', type=str, default="https://rss-updater-pkpovjepjq-wl.a.run.app",
                        help='Base URL for the API endpoint')
    args = parser.parse_args()

    # Run the feed processing with the provided URL or default
    process_feed(args.url)
