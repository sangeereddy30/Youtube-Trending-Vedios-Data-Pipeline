from googleapiclient.discovery import build
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timezone
import logging
from config import YOUTUBE_API_KEY, MONGO_URI, DB_NAME, COLLECTION_NAME, REGION_CODE

# ✅ Log file path corrected
logging.basicConfig(filename="pipeline.log", level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

def extract_trending_videos():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=REGION_CODE,
        maxResults=20
    )
    response = request.execute()
    return response['items']

def transform_data(items):
    data = []
    for item in items:
        data.append({
            "video_id": item['id'],
            "title": item['snippet']['title'],
            "channel": item['snippet']['channelTitle'],
            "publishedAt": item['snippet']['publishedAt'],
            "category": item['snippet'].get('categoryId'),
            "views": int(item['statistics'].get('viewCount', 0)),
            "likes": int(item['statistics'].get('likeCount', 0)),
            "comments": int(item['statistics'].get('commentCount', 0)),
            "fetchedAt": datetime.now(timezone.utc)
        })
    return pd.DataFrame(data)

def load_to_mongodb(df):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Optional: clean out old data
    # collection.delete_many({})  # uncomment if you want fresh data every time

    collection.insert_many(df.to_dict("records"))
    print(f"✅ Inserted {len(df)} new records into MongoDB.")


def main():
    try:
        logging.info("🚀 Starting YouTube ETL Pipeline...")
        items = extract_trending_videos()
        df = transform_data(items)
        load_to_mongodb(df)
        logging.info("✅ Pipeline executed successfully.")
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
