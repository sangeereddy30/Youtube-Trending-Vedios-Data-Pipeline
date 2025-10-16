import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# -------------------- MongoDB Loader --------------------
@st.cache_data
def load_data():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    return df


# -------------------- Streamlit Dashboard --------------------
st.set_page_config(page_title="YouTube Trending Dashboard", layout="wide")
st.title("📊 YouTube Trending Dashboard")

# ✅ Add Refresh Button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()


# -------------------- Load Data --------------------
try:
    df = load_data()
    st.success("✅ Data loaded successfully from MongoDB Atlas!")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

if df.empty:
    st.warning("No data found in MongoDB.")
    st.stop()

# -------------------- Data Preprocessing --------------------
df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
df["fetchedAt"] = pd.to_datetime(df["fetchedAt"], errors="coerce")

# ✅ Keep only the latest record for each video
df = df.sort_values(by=["title", "fetchedAt"], ascending=[True, False])
df = df.drop_duplicates(subset="title", keep="first")

# Ensure numeric fields are numbers
df["comments"] = pd.to_numeric(df["comments"], errors="coerce").fillna(0)
df["views"] = pd.to_numeric(df["views"], errors="coerce").fillna(0)
df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0)

# -------------------- Sidebar Filters --------------------
st.sidebar.header("🎯 Filters")
channels = sorted(df["channel"].dropna().unique())
selected_channel = st.sidebar.selectbox("Select a Channel", ["All"] + list(channels))

if selected_channel != "All":
    df = df[df["channel"] == selected_channel]

# -------------------- Top 10 Videos --------------------
st.subheader("🎬 Top 10 Most Viewed Videos")
top_videos = df.sort_values("views", ascending=False).head(10)
st.table(top_videos[["title", "channel", "views", "likes", "comments"]])

# -------------------- Charts --------------------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        top_videos,
        x="title",
        y="views",
        color="channel",
        title="Top 10 Videos by Views",
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(
        df,
        x="views",
        y="likes",
        color="channel",
        size="comments",
        hover_name="title",
        title="Views vs Likes (Bubble Chart)",
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------- Update Timestamp --------------------
if "fetchedAt" in df.columns and not df["fetchedAt"].isna().all():
    st.caption(f"🕓 Last Updated: {df['fetchedAt'].max()}")
else:
    st.caption("🕓 Last Updated: N/A")
