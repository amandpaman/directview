import streamlit as st
from youtubesearchpython import VideosSearch

# App Title
st.title("🎬 YouTube Search + Embed (No API)")

# Tab Layout
tab1, tab2 = st.tabs(["🔍 Search by Keyword", "📺 Paste URL"])

# TAB 1: Search by Keyword
with tab1:
    st.subheader("Search YouTube Videos")
    search_query = st.text_input("Enter a keyword (e.g., 'cute cats'):")
    
    if search_query:
        st.write(f"🔎 Showing results for: **'{search_query}'**")
        videos = VideosSearch(search_query, limit=5).result()["result"]
        
        for video in videos:
            st.write(f"### {video['title']}")
            st.video(video['link'])
            st.markdown(f"📺 **Channel:** {video['channel']['name']} | ⏱️ **Duration:** {video['duration']}")
            st.write("---")

# TAB 2: Direct URL Embed
with tab2:
    st.subheader("Paste a YouTube URL")
    video_url = st.text_input("Paste here (e.g., https://youtu.be/dQw4w9WgXcQ):")
    
    if video_url:
        if "youtube.com" in video_url or "youtu.be" in video_url:
            st.video(video_url)
        else:
            st.error("❌ Invalid YouTube URL. Try again!")
