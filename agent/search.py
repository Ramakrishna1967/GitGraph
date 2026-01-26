"""Search agent - simplified to avoid rate limits."""

from typing import List
import time

from config import settings
from db import pinecone_client, neo4j_client, RepoResult


# Simple cache
_cache = {}
_cache_ttl = 300


def search_repos(query: str, top_k: int = 5) -> dict:
    """Search repositories using hybrid vector + graph approach."""
    
    # Check cache first
    cache_key = f"{query}_{top_k}"
    if cache_key in _cache:
        cached_time, cached_result = _cache[cache_key]
        if time.time() - cached_time < _cache_ttl:
            print(f"Returning cached result for: {query}")
            return cached_result
    
    print(f"\nSearching for: {query}")
    
    # Simple intent detection without API call
    packages = []
    keywords = ["langchain", "openai", "pydantic", "fastapi", "streamlit", "transformers", "llama", "chroma", "pinecone"]
    for word in keywords:
        if word.lower() in query.lower():
            packages.append(word)
    
    is_compatibility = any(x in query.lower() for x in ["works with", "compatible", "for", "with"])
    
    print(f"  Intent: {'Compatibility' if is_compatibility else 'Semantic'}")
    if packages:
        print(f"  Detected packages: {packages}")
    
    # Vector search
    print("  Running vector search...")
    vector_results = pinecone_client.search(query, top_k=top_k)
    
    # Graph search for dependencies
    graph_results = []
    if packages:
        print(f"  Running graph search...")
        for package in packages:
            graph_results.extend(
                neo4j_client.find_repos_depending_on(package, limit=top_k)
            )
    
    # Combine results
    print("  Combining results...")
    all_results = {}
    
    for repo in vector_results:
        all_results[repo.full_name] = repo
    
    for repo in graph_results:
        if repo.full_name in all_results:
            all_results[repo.full_name].score += 0.5
        else:
            all_results[repo.full_name] = repo
    
    final_results = sorted(
        all_results.values(),
        key=lambda x: x.score,
        reverse=True
    )[:top_k]
    
    # Simple explanation without API call
    if final_results:
        top_repo = final_results[0]
        explanation = f"Found {len(final_results)} repositories matching '{query}'. Top result: {top_repo.name} with {top_repo.stars:,} stars."
    else:
        explanation = f"No repositories found matching '{query}'."
    
    print("  Search complete!\n")
    
    result = {
        "query": query,
        "results": final_results,
        "explanation": explanation,
        "search_strategy": "hybrid" if is_compatibility else "semantic"
    }
    
    # Save to cache
    _cache[cache_key] = (time.time(), result)
    
    return result


def format_results(search_response: dict) -> str:
    """Format search results for display."""
    output = []
    output.append(f"Search: {search_response['query']}")
    output.append(f"Strategy: {search_response['search_strategy']}")
    output.append(f"\n{search_response['explanation']}\n")
    output.append("=" * 60)
    output.append("\nTop Results:\n")
    
    for i, repo in enumerate(search_response['results'], 1):
        output.append(f"{i}. {repo.name}")
        output.append(f"   {repo.stars:,} stars | {repo.url}")
        if repo.description:
            output.append(f"   {repo.description}")
        output.append(f"   Relevance: {repo.score:.2f}\n")
    
    return "\n".join(output)
