import streamlit as st
from youtubesearchpython import VideosSearch

st.set_page_config(page_title="📺 Embedded YouTube Viewer", layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🔍 YouTube Viewer (Embedded Search)")

query = st.text_input("Search Videos", placeholder="e.g. relaxing music, Python tutorial")

if query:
    try:
        results = VideosSearch(query, limit=5).result()['result']
        for video in results:
            title = video['title']
            channel = video['channel']['name']
            views = video['viewCount']['short']
            published = video['publishedTime']
            video_id = video['id']
            embed_url = f"https://www.youtube.com/embed/{video_id}"

            with st.container():
                st.markdown(f"### {title}")
                st.markdown(f"📺 **{channel}**  •  👁 {views}  •  🕓 {published}")
                st.components.v1.iframe(embed_url, height=300)
                st.markdown("---")

    except Exception as e:
        st.error("🚫 Error fetching videos. Check your proxy or internet.")
        st.code(str(e))
