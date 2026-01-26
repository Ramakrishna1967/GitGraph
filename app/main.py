"""
GitGraph RAG - Streamlit Frontend
Hybrid search engine for GitHub repository discovery.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from agent.search import search_repos

# Page config
st.set_page_config(
    page_title="GITGRAPH",
    page_icon="G",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .repo-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        background: #f9f9f9;
    }
    .repo-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0366d6;
    }
    .repo-stats {
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">GITGRAPH</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hybrid Search Engine for GitHub Repository Discovery</div>', unsafe_allow_html=True)

# Search bar
query = st.text_input(
    "Search for repositories",
    placeholder="Try: 'PDF parser for langchain' or 'data validation library'",
    key="search_query"
)

# Number of results slider
top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

# Search button
if st.button("Search", type="primary") or query:
    if query:
        with st.spinner("Searching..."):
            try:
                response = search_repos(query, top_k=top_k)
                
                st.success(f"**{response['explanation']}**")
                st.info(f"**Search Strategy:** {response['search_strategy'].title()}")
                
                st.markdown("### Top Results")
                
                for i, repo in enumerate(response['results'], 1):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. [{repo.name}]({repo.url})")
                            if repo.description:
                                st.markdown(f"*{repo.description}*")
                        
                        with col2:
                            st.metric("Stars", f"{repo.stars:,}")
                            st.metric("Score", f"{repo.score:.2f}")
                        
                        if repo.language:
                            st.caption(f"Language: {repo.language}")
                        
                        st.divider()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a search query")

# Sidebar
with st.sidebar:
    st.markdown("## About")
    st.markdown("""
    **GITGRAPH** combines:
    - **Semantic Search** (Pinecone + Gemini)
    - **Graph Traversal** (Neo4j)
    - **AI Intelligence** (Gemini)
    
    ### How it works:
    1. Understands your query intent
    2. Searches by meaning (not just keywords)
    3. Finds compatible dependencies
    4. Ranks by relevance
    """)
