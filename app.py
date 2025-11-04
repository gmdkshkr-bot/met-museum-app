import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import time

# Page setup
st.set_page_config(
    page_title="Met Museum Explorer",
    page_icon="🎨",
    layout="wide"
)

# Title
st.title("🎨 Met Museum Art Explorer")
st.write("Explore artworks from The Metropolitan Museum of Art")

# Sidebar for search
with st.sidebar:
    st.header("Search")
    search_query = st.text_input("Enter search term", placeholder="e.g., Van Gogh, samurai")
    max_results = st.slider("Number of results", 5, 20, 10)
    search_button = st.button("🔍 Search", type="primary")

# API base URL
BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

# Search function
def search_artworks(query, max_results):
    try:
        # Search API
        search_url = f"{BASE_URL}/search?q={query}"
        response = requests.get(search_url, timeout=10)
        data = response.json()
        
        if not data.get('objectIDs'):
            return []
        
        # Get artwork details
        artworks = []
        object_ids = data['objectIDs'][:max_results]
        
        progress = st.progress(0)
        for idx, obj_id in enumerate(object_ids):
            try:
                obj_url = f"{BASE_URL}/objects/{obj_id}"
                obj_response = requests.get(obj_url, timeout=5)
                artwork = obj_response.json()
                
                if artwork.get('primaryImage'):
                    artworks.append(artwork)
                
                progress.progress((idx + 1) / len(object_ids))
                time.sleep(0.1)
            except:
                continue
        
        progress.empty()
        return artworks
    except:
        return []

# Main area
if search_button and search_query:
    with st.spinner("Searching..."):
        results = search_artworks(search_query, max_results)
    
    if results:
        st.success(f"Found {len(results)} artworks!")
        
        # Display in columns
        cols = st.columns(3)
        for idx, artwork in enumerate(results):
            col = cols[idx % 3]
            with col:
                st.image(artwork['primaryImage'], use_container_width=True)
                st.subheader(artwork.get('title', 'Untitled'))
                st.write(f"**Artist:** {artwork.get('artistDisplayName', 'Unknown')}")
                st.write(f"**Date:** {artwork.get('objectDate', 'N/A')}")
                if artwork.get('objectURL'):
                    st.link_button("View on Met Website", artwork['objectURL'])
                st.divider()
    else:
        st.error("No artworks found. Try a different search term.")
else:
    st.info("👈 Enter a search term in the sidebar and click Search!")
    st.write("### Try searching for:")
    st.write("- Van Gogh")
    st.write("- Monet")
    st.write("- Japanese art")
    st.write("- Ancient Egypt")
