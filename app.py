import streamlit as st
from pytube import Search

st.title("🎬 YouTube Video Search")

# Search by keyword
search_query = st.text_input("Search YouTube videos")

if search_query:
    try:
        st.write(f"🔎 Results for: **'{search_query}'**")
        
        # Get top 5 video results
        videos = Search(search_query).results[:5]
        
        for video in videos:
            st.write(f"### {video.title}")
            st.video(video.watch_url)
            st.caption(f"👤 Channel: {video.author} | ⏱️ {video.length} seconds")
            st.write("---")
            
    except Exception as e:
        st.error(f"Error loading videos. Try again later. ({str(e)})")

# Direct URL embed fallback
st.write("---")
st.subheader("...or paste a YouTube URL")
video_url = st.text_input("Paste URL here (e.g., https://youtu.be/dQw4w9WgXcQ)")

if video_url:
    if "youtube.com" in video_url or "youtu.be" in video_url:
        st.video(video_url)
    else:
        st.error("❌ Invalid YouTube URL")
