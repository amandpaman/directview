import streamlit as st
from youtubesearchpython import VideosSearch

st.set_page_config(page_title="YouTube Viewer", layout="wide")
st.title("🎬 YouTube Viewer Without Pasting URLs")

query = st.text_input("🔍 Search for a video", placeholder="Type something like 'AI songs'")

if query:
    with st.spinner("Searching YouTube..."):
        try:
            results = VideosSearch(query, limit=10).result()['result']

            for video in results:
                title = video['title']
                duration = video['duration']
                views = video['viewCount']['short']
                published = video['publishedTime']
                channel = video['channel']['name']
                thumbnail = video['thumbnails'][0]['url']
                link = video['link']

                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(thumbnail, use_column_width=True)
                with col2:
                    st.markdown(f"### {title}")
                    st.markdown(f"⏱ {duration} | 👀 {views} | 📅 {published}")
                    st.markdown(f"📺 Channel: {channel}")
                    st.video(link)

                st.markdown("---")
        except Exception as e:
            st.error("❌ Something went wrong while fetching videos.")
            st.code(str(e))
