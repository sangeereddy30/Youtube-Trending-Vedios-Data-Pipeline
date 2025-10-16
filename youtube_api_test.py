from googleapiclient.discovery import build
import pandas as pd

# Replace with your API key
API_KEY = "youtubeAPI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Initialize YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# Request trending videos
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="IN",   # Change if needed
    maxResults=20
)
response = request.execute()

# Extract useful fields
data = []
for item in response['items']:
    data.append({
        "Title": item['snippet']['title'],
        "Channel": item['snippet']['channelTitle'],
        "Views": item['statistics'].get('viewCount', 0),
        "Likes": item['statistics'].get('likeCount', 0),
        "Comments": item['statistics'].get('commentCount', 0),
    })

df = pd.DataFrame(data)
print(df)

