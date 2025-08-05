import os

# Set your proxy settings here
proxy = "http://username:password@10.8.0.1:8080"

# Set proxy environment variables globally
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

# Run your Streamlit app
os.system("streamlit run youtube_viewer.py")
