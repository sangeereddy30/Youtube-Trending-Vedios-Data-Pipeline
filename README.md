# Youtube-Trending-Videos-Data-Pipeline
🎥 YouTube Trending ETL Dashboard

An end-to-end Data Engineering & Visualization project that extracts trending YouTube video data using the YouTube Data API, stores it in MongoDB Atlas, and visualizes insights using an interactive Streamlit Dashboard.

🚀 Project Overview

This project automates the entire ETL (Extract–Transform–Load) workflow for YouTube trending videos.
It then provides a live analytics dashboard built with Streamlit to explore metrics such as views, likes, comments, and channel performance.

🧩 Tech Stack
Category	Tools / Technologies
Programming Language	Python
Data Extraction	YouTube Data API v3
Data Storage	MongoDB Atlas
Data Visualization	Streamlit, Plotly
Data Handling	Pandas
Scheduling (Optional)	Apache Airflow / Windows Task Scheduler
⚙️ Project Architecture


        ┌────────────────────┐
        │  YouTube API v3    │
        └─────────┬──────────┘
                  │ (Extract)
                  ▼
        ┌────────────────────┐
        │   Transform Data   │  ← Clean & Format JSON
        └─────────┬──────────┘
                  │ (Load)
                  ▼
        ┌────────────────────┐
        │ MongoDB Atlas (DB) │
        └─────────┬──────────┘
                  │ (Read)
                  ▼
        ┌────────────────────┐
        │ Streamlit Dashboard│
        └────────────────────┘

        




🧠 Features

✅ Automated ETL pipeline to fetch YouTube trending data
✅ Real-time dashboard built with Streamlit
✅ MongoDB Atlas for cloud-based storage
✅ Interactive charts with Plotly
✅ Channel-based filtering and analysis
✅ Top 10 most-viewed video table
✅ Refresh button for live updates


# 5️⃣ Launch the dashboard
streamlit run youtube_dashboard.py

🧭 How the ETL Works

Extract: Fetch trending videos using the YouTube Data API v3.

Transform: Clean, normalize, and convert the data into a structured format.

Load: Store the processed data into MongoDB Atlas.

Visualize: Use Streamlit to explore metrics like views, likes, and engagement.

📊 Dashboard Preview

Dashboard Highlights:

🎬 Top 10 most viewed videos

📈 Interactive bar and bubble charts

🎛 Channel-based filtering

🔄 Data refresh support

🕓 Last updated timestamp

🧰 Requirements

Python 3.8+

Streamlit

Pandas

Plotly

Pymongo


⭐ Future Enhancements

Add time-series analysis for daily trending variations

Integrate Airflow for automated daily ETL

Add sentiment analysis on video titles and comments

Add data export options (CSV/Excel)
