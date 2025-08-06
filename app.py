import streamlit as st
from youtubesearchpython import VideosSearch

st.title("🎬 YouTube Search + Embed")

search_query = st.text_input("Search YouTube videos")

if search_query:
    try:
        videos = VideosSearch(search_query, limit=5).result()["result"]
        
        for video in videos:
            st.write(f"### {video['title']}")
            st.video(video['link'])
            st.caption(f"Channel: {video['channel']['name']} | Duration: {video['duration']}")
            st.write("---")
            
    except Exception as e:
        st.error(f"Error loading videos. Try again later. ({str(e)})")
