from googleapiclient.discovery import build
import pandas as pd
import time
import matplotlib.pyplot as plt

API_KEY = "AIzaSyCMETYE1qmlMKzIms8ZGrU7qLwAIo6XkLs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def get_trending_videos(max_pages=3, region_code="IN"):
    videos = []
    next_page_token = None

    for _ in range(max_pages):
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})

            videos.append({
                "Video_ID": item["id"],
                "Title": snippet["title"],
                "Channel": snippet["channelTitle"],
                "Category_ID": snippet["categoryId"],
                "PublishedAt": snippet["publishedAt"],
                "Duration": content.get("duration", ""),
                "Views": int(stats.get("viewCount", 0)),
                "Likes": int(stats.get("likeCount", 0)),
                "Comments": int(stats.get("commentCount", 0))
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

        time.sleep(1)  # small delay to avoid quota issues

    return pd.DataFrame(videos)

df = get_trending_videos(max_pages=2)
print(df.head())
print("\nTotal Videos Fetched:", len(df))


#clean the dATA

# Check for missing values
print(df.isnull().sum())

# Fill missing numeric values with 0
df["Likes"] = df["Likes"].fillna(0)
df["Comments"] = df["Comments"].fillna(0)


# Convert published date to datetime
df["PublishedAt"] = pd.to_datetime(df["PublishedAt"])

# Sort by views
df = df.sort_values(by="Views", ascending=False).reset_index(drop=True)

print(df.head())




top_channels = df["Channel"].value_counts().head(10)

plt.figure(figsize=(10,5))
top_channels.plot(kind="bar", color="skyblue")
plt.title("Top 10 Channels in Trending Videos")
plt.xlabel("Channel")
plt.ylabel("Count in Trending List")
plt.show()


