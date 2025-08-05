import streamlit as st
import requests
import json
from urllib.parse import urlparse, parse_qs
import re

# Configure the page
st.set_page_config(
    page_title="YouTube Player",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF0000;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .video-container {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        margin: 1rem 0;
    }
    .search-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .video-info {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    if not url:
        return None
    
    # Handle different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If it's just a video ID
    if len(url) == 11 and url.isalnum():
        return url
    
    return None

def get_video_info(video_id):
    """Get basic video information (this is a mock function since we don't have API key)"""
    # In a real application, you would use YouTube Data API v3
    # For demo purposes, we'll return mock data
    return {
        "title": f"Video {video_id}",
        "description": "This would contain the actual video description from YouTube API",
        "channel": "Channel Name",
        "views": "1,234,567 views",
        "likes": "12,345 likes"
    }

def create_embed_url(video_id, autoplay=False, start_time=0):
    """Create YouTube embed URL"""
    embed_url = f"https://www.youtube.com/embed/{video_id}?"
    params = []
    
    if autoplay:
        params.append("autoplay=1")
    if start_time > 0:
        params.append(f"start={start_time}")
    
    params.extend([
        "rel=0",  # Don't show related videos from other channels
        "modestbranding=1",  # Minimal YouTube branding
        "fs=1",  # Allow fullscreen
        "cc_load_policy=0",  # Don't show captions by default
        "iv_load_policy=3",  # Hide annotations
        "autohide=1"  # Auto-hide controls
    ])
    
    return embed_url + "&".join(params)

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🎥 YouTube Player</h1>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Video quality selector
        quality = st.selectbox(
            "Video Quality",
            ["Auto", "720p", "480p", "360p", "240p"],
            index=0
        )
        
        # Playback options
        autoplay = st.checkbox("Autoplay", value=False)
        
        # Volume control
        volume = st.slider("Volume", 0, 100, 50)
        
        # Playback speed
        speed = st.selectbox(
            "Playback Speed",
            ["0.25x", "0.5x", "0.75x", "1x", "1.25x", "1.5x", "2x"],
            index=3
        )
        
        st.markdown("---")
        
        # Saved videos (mock data)
        st.header("📚 Saved Videos")
        saved_videos = [
            "dQw4w9WgXcQ",  # Rick Roll
            "9bZkp7q19f0",  # Gangnam Style
            "kJQP7kiw5Fk"   # Despacito
        ]
        
        for i, vid_id in enumerate(saved_videos):
            if st.button(f"Video {i+1}", key=f"saved_{i}"):
                st.session_state.current_video = vid_id

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search/URL input section
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.subheader("🔍 Enter YouTube URL or Video ID")
        
        # Input methods
        input_method = st.radio(
            "Input Method:",
            ["YouTube URL", "Video ID", "Search Term"],
            horizontal=True
        )
        
        if input_method == "YouTube URL":
            user_input = st.text_input(
                "Paste YouTube URL:",
                placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                help="Paste any YouTube video URL"
            )
        elif input_method == "Video ID":
            user_input = st.text_input(
                "Enter Video ID:",
                placeholder="dQw4w9WgXcQ",
                help="Enter the 11-character video ID"
            )
        else:
            user_input = st.text_input(
                "Search Term:",
                placeholder="Enter search term",
                help="Search functionality would require YouTube API integration"
            )
            if user_input:
                st.info("🔍 Search functionality requires YouTube Data API integration. For now, please use direct URLs or Video IDs.")
        
        # Start time input
        start_time = st.number_input(
            "Start time (seconds)",
            min_value=0,
            value=0,
            help="Start the video at a specific time"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process input and display video
        if user_input:
            if input_method in ["YouTube URL", "Video ID"]:
                video_id = extract_video_id(user_input) if input_method == "YouTube URL" else user_input
                
                if video_id:
                    st.session_state.current_video = video_id
                    st.success(f"✅ Video ID extracted: {video_id}")
                    
                    # Create embed URL
                    embed_url = create_embed_url(video_id, autoplay, start_time)
                    
                    # Display video
                    st.markdown('<div class="video-container">', unsafe_allow_html=True)
                    st.markdown(f"""
                    <iframe 
                        width="100%" 
                        height="400" 
                        src="{embed_url}" 
                        frameborder="0" 
                        allowfullscreen>
                    </iframe>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Video information section
                    st.markdown('<div class="video-info">', unsafe_allow_html=True)
                    st.subheader("📽️ Video Information")
                    
                    # Get video info (mock data for demo)
                    video_info = get_video_info(video_id)
                    
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.write(f"**Title:** {video_info['title']}")
                        st.write(f"**Channel:** {video_info['channel']}")
                    with col_info2:
                        st.write(f"**Views:** {video_info['views']}")
                        st.write(f"**Likes:** {video_info['likes']}")
                    
                    with st.expander("Description"):
                        st.write(video_info['description'])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                else:
                    st.error("❌ Invalid YouTube URL or Video ID. Please check your input.")
    
    with col2:
        # Video history and features
        st.subheader("📊 App Features")
        
        # Current video info
        if 'current_video' in st.session_state:
            st.info(f"🎬 Current Video: {st.session_state.current_video}")
        
        # Feature list
        features = [
            "🎥 YouTube video embedding",
            "🔗 Multiple URL format support",
            "⏰ Custom start time",
            "🎛️ Playback controls",
            "📱 Responsive design",
            "💾 Video history (mock)",
            "🔍 Search integration (API needed)",
            "📚 Playlist support (future)",
            "⭐ Favorites system (future)",
            "🌙 Dark/Light theme (future)"
        ]
        
        for feature in features:
            st.write(feature)
        
        st.markdown("---")
        
        # Statistics (mock data)
        st.subheader("📈 Statistics")
        st.metric("Videos Watched", "42", "↗️ 12")
        st.metric("Total Watch Time", "2h 34m", "↗️ 45m")
        st.metric("Favorite Genre", "Music", "🎵")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Clear Current Video"):
            if 'current_video' in st.session_state:
                del st.session_state.current_video
                st.rerun()
        
        if st.button("📋 Copy Current URL"):
            if 'current_video' in st.session_state:
                url = f"https://www.youtube.com/watch?v={st.session_state.current_video}"
                st.code(url)
                st.success("URL ready to copy!")
        
        # Popular videos (mock data)
        st.subheader("🔥 Popular Videos")
        popular_videos = {
            "Rick Astley - Never Gonna Give You Up": "dQw4w9WgXcQ",
            "PSY - Gangnam Style": "9bZkp7q19f0",
            "Luis Fonsi - Despacito": "kJQP7kiw5Fk"
        }
        
        for title, vid_id in popular_videos.items():
            if st.button(title, key=f"popular_{vid_id}"):
                st.session_state.current_video = vid_id
                st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem 0;">
        <p>🎥 YouTube Streamlit Player | Built with ❤️ using Streamlit</p>
        <p><small>Note: This app uses YouTube's embed player. For full API integration, you'll need a YouTube Data API key.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
